import math
import random
from enum import Enum
from collections import deque
import gc

import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical
import torch.nn.functional as F
import torch.optim as optim

from GameSim.Input.PPO import PPOAgent, CardEncoder


class RunningMeanStd:
    """
    Tracks running mean and standard deviation of observations using Welford's online algorithm.
    This is used for normalizing observations to have zero mean and unit variance.
    """
    def __init__(self, shape, epsilon=1e-4):
        """
        Args:
            shape: Shape of the observations to track
            epsilon: Small constant for numerical stability
        """
        self.mean = np.zeros(shape, dtype=np.float32)
        self.var = np.ones(shape, dtype=np.float32)
        self.count = epsilon
        self.epsilon = epsilon

    def update(self, batch):
        """
        Update running statistics with a batch of observations.
        Uses Welford's online algorithm for numerical stability.

        Args:
            batch: Batch of observations (can be single observation or multiple)
        """
        if isinstance(batch, torch.Tensor):
            batch = batch.detach().cpu().numpy()

        # Handle single observation
        if batch.ndim == 1:
            batch = batch.reshape(1, -1)

        batch_count = batch.shape[0]
        if batch_count == 0:
            return

        batch_mean = np.mean(batch, axis=0)
        batch_var = np.var(batch, axis=0)

        self.update_from_moments(batch_mean, batch_var, batch_count)

    def update_from_moments(self, batch_mean, batch_var, batch_count):
        """
        Update statistics from batch moments using parallel algorithm.

        Args:
            batch_mean: Mean of the batch
            batch_var: Variance of the batch
            batch_count: Number of samples in the batch
        """
        delta = batch_mean - self.mean
        total_count = self.count + batch_count

        new_mean = self.mean + delta * batch_count / total_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + np.square(delta) * self.count * batch_count / total_count
        new_var = M2 / total_count

        self.mean = new_mean
        self.var = new_var
        self.count = total_count

    def normalize(self, obs, update=True):
        """
        Normalize observations using current statistics.

        Args:
            obs: Observations to normalize (numpy array or torch tensor)
            update: Whether to update running statistics with this observation

        Returns:
            Normalized observations in the same format as input
        """
        is_tensor = isinstance(obs, torch.Tensor)
        device = obs.device if is_tensor else None

        if is_tensor:
            obs_np = obs.detach().cpu().numpy()
        elif isinstance(obs, dict):
            obs_np = np.array(obs)
        else:
            obs_np = obs

        if update:
            self.update(obs_np)

        # Normalize
        normalized = (obs_np - self.mean) / np.sqrt(self.var + self.epsilon)

        # Convert back to tensor if input was tensor
        if is_tensor:
            normalized = torch.from_numpy(normalized).float().to(device)

        return normalized


class ActorCriticLSTM(nn.Module):
    """
    An Actor-Critic network that uses an LSTM to process sequential battle states.
    """
    def __init__(self, input_dim, lstm_hidden_dim, total_bt_actions, total_cb_actions):
        super().__init__()

        # This layer processes the sequence of states within a battle.
        self.lstm_hidden_dim = lstm_hidden_dim
        self.num_layers = 1
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=self.num_layers,
            batch_first=True  # Important for handling single-item batches
        )

        # --- Shared Base Network ---
        # This network now processes the LSTM's output combined with static features (like the deck embedding).
        combined_feature_dim = lstm_hidden_dim
        leaky_relu_slope = 0.02
        network_size = 256

        xavier_gain = nn.init.calculate_gain('leaky_relu', leaky_relu_slope)
        first_layer = nn.Linear(combined_feature_dim, network_size)
        nn.init.xavier_uniform_(first_layer.weight, gain=xavier_gain)
        second_layer = nn.Linear(network_size, network_size // 2)
        nn.init.xavier_uniform_(second_layer.weight, gain=xavier_gain)
        self.base_network = nn.Sequential(
            first_layer,
            nn.LeakyReLU(leaky_relu_slope),
            second_layer,
            nn.LeakyReLU(leaky_relu_slope),
        )

        # --- Actor Heads ---
        self.actor_bt_head = nn.Linear(network_size // 2, total_bt_actions)
        nn.init.xavier_uniform_(self.actor_bt_head.weight, gain=xavier_gain)
        # The Card Build head does not use the LSTM, it uses a separate simple network.
        cb_layer = nn.Linear(input_dim, network_size // 2)
        nn.init.xavier_uniform_(cb_layer.weight, gain=xavier_gain)
        self.cb_base_network = nn.Sequential(
            cb_layer, # Only sees static deck/player info
            nn.LeakyReLU(leaky_relu_slope)
        )
        self.actor_cb_head = nn.Linear(network_size // 2, total_cb_actions)
        nn.init.xavier_uniform_(self.actor_cb_head.weight, gain=xavier_gain)

        # --- Critic Head ---
        self.critic_head = nn.Linear(network_size // 2, 1)
        nn.init.xavier_uniform_(self.critic_head.weight, gain=xavier_gain)

    def forward(self, features, hidden_state, stage):
        """
        Performs a forward pass. Note the new 'hidden_state' argument.
        """
        if stage == PPOAgent.GameStage.BATTLE:
            # Pass dynamic features and the previous hidden state through the LSTM.
            # We add a sequence dimension (1) to the input tensor.
            features = features.unsqueeze(0)
            lstm_out, new_hidden_state = self.lstm(features, hidden_state)

            # The output needs to be squeezed to remove the sequence dimension before concatenation.
            lstm_out = lstm_out.squeeze(0).squeeze(0)

            # Pass the combined vector through the base network.
            base_output = self.base_network(lstm_out)

        elif stage == PPOAgent.GameStage.CARD_BUILD:
            # Card building is not sequential, so we bypass the LSTM.
            # The new_hidden_state is None because we are not in a battle sequence.
            base_output = self.cb_base_network(features)
            new_hidden_state = None
        else:
            raise ValueError(f"Unknown stage: {stage}")

        # --- Get Action Logits and State Value ---
        state_value = self.critic_head(base_output)
        if stage == PPOAgent.GameStage.BATTLE:
            action_logits = self.actor_bt_head(base_output)
        else: # CARD_BUILD
            action_logits = self.actor_cb_head(base_output)

        return action_logits, state_value.squeeze(-1), new_hidden_state

    def sample_action(self, stage, features, hidden_state, action_mask):
        # --- Get Action Logits and State Value ---
        action_logits, state_value, new_hidden_state = self.forward(features, hidden_state, stage)

        masked_logits = torch.where(
            action_mask,
            action_logits,
            torch.tensor(-1e9)
        )

        # --- Sample Action ---
        action_dist = Categorical(logits=masked_logits)
        action = action_dist.sample()

        log_prob = action_dist.log_prob(action).unsqueeze(-1)

        return action, log_prob, state_value, new_hidden_state, action_dist.probs

class LSTMPPOAgent(PPOAgent):
    STATE_KEYS = ["player", 'strategic', 'deck', 'hand']
    def __init__(self, num_actions, card_feature_length, player_feature_length, enemy_feature_length, strategic_feature_length,
                 filepath, learning_enabled=True, save_model=True, visualizer=None):
        super().__init__(num_actions, card_feature_length, player_feature_length, enemy_feature_length, strategic_feature_length, filepath, learning_enabled=learning_enabled, save_weights=save_model, visualizer=visualizer)

        self.best_avg_reward = -math.inf
        # Define the dimensions for the new network
        self.lstm_hidden_dim = 256

        # --- Initialize the New Network ---
        self.actor_critic = ActorCriticLSTM(
            input_dim=self.embed_dim,
            lstm_hidden_dim=self.lstm_hidden_dim,
            total_bt_actions=(self.max_cards * self.max_enemies) + self.other_actions,
            total_cb_actions=self.max_card_choices
        ).to(self.device)

        self.old_network = ActorCriticLSTM(
            input_dim=self.embed_dim,
            lstm_hidden_dim=self.lstm_hidden_dim,
            total_bt_actions=(self.max_cards * self.max_enemies) + self.other_actions,
            total_cb_actions=self.max_card_choices
        ).to(self.device)

        self.old_network.load_state_dict(self.actor_critic.state_dict())

        self.params = list(self.actor_critic.parameters()) + list(self.state_encoder.parameters())
        self.optimizer = optim.Adam(self.params, lr=self.lr)
        self.initial_lr = self.lr
        # self.lr_scheduler = optim.lr_scheduler.CyclicLR(self.optimizer,
        #                                                 self.initial_lr / 5,
        #                                                 self.initial_lr * 2,
        #                                                 step_size_up=100)

        self.lr_scheduler = optim.lr_scheduler.LinearLR(self.optimizer,
                                                        start_factor=1.0,
                                                        end_factor=0.05,
                                                        total_iters=2000)

        # --- Add a placeholder for the hidden state ---
        self.hidden_state = None

        self.memory['hidden_states'] = []
        self.memory['cell_states'] = []

        self.sequence_length = 64

        # --- Observation Normalization ---
        self.obs_norms = {
            'player': RunningMeanStd(shape=player_feature_length),
            'strategic': RunningMeanStd(shape=strategic_feature_length),
            'enemies': RunningMeanStd(shape=enemy_feature_length),  # normalizes per-enemy-feature
            # deck and hand use the same card feature space
            'cards': RunningMeanStd(shape=card_feature_length),
        }

    def reset_hidden_state(self):
        """Call this at the beginning of each battle."""
        # Initialize a zero hidden state and cell state for the LSTM
        self.hidden_state = (
            torch.zeros(1, 1, self.lstm_hidden_dim).to(self.device),
            torch.zeros(1, 1, self.lstm_hidden_dim).to(self.device)
        )

    def _normalize_state_dict(self, state_tensors: dict, update: bool) -> dict:
        """
        Normalize each component of the state dictionary using its own RunningMeanStd.
        Operates on a dict of tensors; returns a new dict with normalized tensors.
        """
        normalized = dict(state_tensors)  # shallow copy — we'll replace values

        for key in self.STATE_KEYS:
            if key not in state_tensors:
                continue
            if key == "deck" or key == "hand":
                norm_key = "cards"
            else:
                norm_key = key

            t = state_tensors[key]
            normalized[key] = torch.tensor(
                self.obs_norms[norm_key].normalize(t, update=update),
                dtype=torch.float32, device=self.device
            )

        # Enemies: shape is (num_enemies, enemy_feature_dim) — normalize per feature across the enemy dim
        if 'enemies' in state_tensors:
            e = state_tensors['enemies']
            normalized['enemies'] = torch.tensor(
                self.obs_norms['enemies'].normalize(e, update=update),
                dtype=torch.float32, device=self.device
            )

        # action_mask and card_choices are not normalized
        return normalized

    def remember(self, stage, state, action, reward, done, log_prob, value, hidden_state):
        """Override the remember method to also store the hidden state."""
        super().remember(stage, state, action, reward, done, log_prob, value)

        # Unpack and store the hidden and cell states
        h, c = hidden_state
        self.memory['hidden_states'].append(h.detach().cpu().numpy())
        self.memory['cell_states'].append(c.detach().cpu().numpy())

    def get_state_from_memory_by_idx(self, idx):
        return self.memory['states'][idx], ((self.memory['hidden_states'][idx], self.memory['cell_states'][idx]) ,self.memory['stages'][idx])

    def choose_action(self, state_tensors):
        """
        Choose action, now passing the hidden state.
        :param state_tensors: A single state dictionary with values of the dictionary converted to tensors.
        """
        normalized_state_tensors = self._normalize_state_dict(state_tensors, update=self.learning_enabled)
        state_tuple, stage, action_mask = self.embed_state(normalized_state_tensors)
        embedded_state = self.state_encoder(*state_tuple)

        self.actor_critic.eval()
        with torch.no_grad():
            # Pass the current hidden state to the network
            action_choice, log_prob, value, new_hidden_state, action_probs = self.actor_critic.sample_action(
                stage, embedded_state, self.hidden_state, action_mask
            )
            # Update the agent's hidden state for the next step
            if stage == self.GameStage.BATTLE:
                self.hidden_state = new_hidden_state

        self.actor_critic.train()
        return action_choice.detach().cpu().item(), log_prob.detach().cpu(), value.detach().cpu(), action_probs.detach().cpu().numpy()

    def _learn(self):
        # self.device = "mps"
        # --- Retrieve all data from memory ---
        actions_arr = np.array(self.memory['actions'])
        rewards_arr = np.array(self.memory['rewards'])
        dones_arr = np.array(self.memory['dones'])
        old_log_probs_arr = np.array(self.memory['log_probs'])
        values_arr = np.array(self.memory['values'])
        stages_arr = self.memory['stages']
        # hidden_states_arr = np.array(self.memory['hidden_states'])
        # cell_states_arr = np.array(self.memory['cell_states'])

        advantages_arr = self._compute_gae_per_episode(rewards_arr, values_arr, dones_arr)
        advantages = torch.tensor(advantages_arr, dtype=torch.float32).to(self.device)

        adv_mean = advantages.mean()
        adv_std = advantages.std()

        if adv_std.isnan() or adv_std < 1e-8:
            print(f"WARNING: Advantage std is {adv_std.item()}, sktipping normalization")
            advantages_all = advantages - adv_mean
        else:
            advantages_all = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # if torch.isnan(advantages_all).any():
        #     print("WARNING: NaN in advantages, skipping this batch")
        #     continue

        value_targets_all = advantages + torch.tensor(values_arr, dtype=torch.float32).to(self.device)

        episode_indices = []
        current_episode_start = 0
        # Find the start index of each episode
        for i in range(len(dones_arr)):
            if dones_arr[i]:
                episode_indices.append(list(range(current_episode_start, i + 1)))
                current_episode_start = i + 1

        losses = []
        grad_norm = 0.0
        clip_frac = 0.0
        sum_policy_loss = 0.0
        sum_value_loss = 0.0
        sum_entropy = 0.0
        sum_clip_frac = 0.0
        sum_grad_norm = 0.0
        sum_adv_std = 0.0
        sum_total_loss = 0.0
        n_updates = 0
        for _ in range(self.learn_epochs):
            # Shuffle the sequences, NOT the individual steps
            random.shuffle(episode_indices)
            policy_loss, value_loss, entropy_loss, batch_advantages, ratios = 0, 0, 0, 0, 0

            for episode in episode_indices:
                episode_len = len(episode)
                if episode_len == 0:
                    continue

                raw_seq = [self.memory['states'][i] for i in episode]

                # Normalize each component across the episode batch (update=False, stats already current)
                batch_deck = torch.tensor(self.obs_norms['cards'].normalize(
                    np.stack([s[0] for s in raw_seq]), update=False), dtype=torch.float32).to(self.device)
                batch_hand = torch.tensor(self.obs_norms['cards'].normalize(
                    np.stack([s[1] for s in raw_seq]), update=False), dtype=torch.float32).to(self.device)
                batch_player = torch.tensor(self.obs_norms['player'].normalize(
                    np.stack([s[2] for s in raw_seq]), update=False), dtype=torch.float32).to(self.device)
                batch_strategic = torch.tensor(self.obs_norms['strategic'].normalize(
                    np.stack([s[3] for s in raw_seq]), update=False), dtype=torch.float32).to(self.device)
                batch_enemies = torch.tensor(self.obs_norms['enemies'].normalize(
                    np.stack([s[4] for s in raw_seq]), update=False), dtype=torch.float32).to(self.device)
                batch_enemy_mask = torch.tensor(
                    np.stack([s[5] for s in raw_seq]), dtype=torch.bool).to(self.device) if raw_seq[0][5] is not None else None

                batch_states = self.state_encoder(batch_deck, batch_hand, batch_player, batch_strategic, batch_enemies, batch_enemy_mask)

                # Get the mini-batch of sequences
                batch_actions = torch.tensor(actions_arr[episode], dtype=torch.long).to(self.device)
                batch_old_log_probs = torch.tensor(old_log_probs_arr[episode], dtype=torch.float32).to(
                    self.device)
                batch_advantages = advantages_all[episode].to(self.device)

                if torch.isnan(batch_advantages).any() or batch_advantages.std() < 1e-6:
                    continue

                batch_value_targets = value_targets_all[episode].to(self.device)
                batch_stages = [stages_arr[i] for i in episode]
                initial_hidden_state = (
                    torch.zeros(self.actor_critic.lstm.num_layers, 1, self.lstm_hidden_dim).to(self.device),
                    torch.zeros(self.actor_critic.lstm.num_layers, 1, self.lstm_hidden_dim).to(self.device)
                )

                # --- Recompute log probabilities using initial hidden states ---
                new_log_prob, new_entropy, values = self._compute_log_prob_lstm_batch(
                    batch_stages, batch_states, batch_actions, initial_hidden_state[0], initial_hidden_state[1]
                )

                # --- Loss Calculation ---
                ratios = torch.exp(new_log_prob - batch_old_log_probs)
                objective = ratios * batch_advantages
                penalty = (torch.abs(batch_advantages) / (2 * self.epsilon)) * ((ratios - 1) ** 2)
                policy_loss = -torch.mean(objective - penalty)

                value_loss = F.mse_loss(values, batch_value_targets)
                entropy_loss = -new_entropy.mean()

                total_loss = policy_loss + self.value_coef * value_loss + self.entropy_coef * entropy_loss
                losses.append(total_loss.item())

                self.optimizer.zero_grad()
                total_loss.backward()
                grad_norm = torch.nn.utils.clip_grad_norm_(self.params, max_norm=0.5).item()
                self.optimizer.step()
                clip_frac = (torch.abs(ratios - 1) > self.epsilon).float().mean().item()

                sum_policy_loss += policy_loss.item()
                sum_value_loss += value_loss.item()
                sum_entropy += -entropy_loss.item()
                sum_clip_frac += clip_frac
                sum_grad_norm += grad_norm
                sum_adv_std += batch_advantages.std().item()
                sum_total_loss += total_loss.item()
                n_updates += 1

            self.lr_scheduler.step()
            self.entropy_coef *= self.entropy_decay

            if self.learn_step_counter % 2 == 0 and isinstance(policy_loss, torch.Tensor):
                print(f"Policy Loss: {policy_loss.item():.4f}")
                print(f"Value Loss: {value_loss.item():.4f}")
                print(f"Entropy: {-entropy_loss.item():.4f}")
                print(f"Clip Fraction: {clip_frac:.2%}")
                print(f"Advantage Std: {batch_advantages.std():.4f}")


        self.old_network.load_state_dict(self.actor_critic.state_dict())
        # Clear memory after learning
        for key in self.memory:
            self.memory[key].clear()

        # Explicit memory cleanup to combat PyTorch memory fragmentation
        gc.collect()
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        elif torch.cuda.is_available():
            torch.cuda.empty_cache()

        avg_loss = sum(losses) / len(losses) if losses else 0.0 # prevent division by 0 if no full episodes
        avg_reward = (sum(rewards_arr) / len(rewards_arr))
        self.losses.append(avg_loss)
        self.rewards.append(avg_reward)

        if self.visualizer and n_updates > 0:
            self.visualizer.log_training_step(
                policy_loss=sum_policy_loss / n_updates,
                value_loss=sum_value_loss / n_updates,
                entropy=sum_entropy / n_updates,
                clip_fraction=sum_clip_frac / n_updates,
                advantage_std=sum_adv_std / n_updates,
                grad_norm=sum_grad_norm / n_updates,
                total_loss=sum_total_loss / n_updates,
                avg_reward=float(avg_reward),
                learn_rate=self.lr_scheduler.get_last_lr()[0],
                entropy_coef=self.entropy_coef,
                learn_step=self.learn_step_counter
            )

        if avg_reward > self.best_avg_reward:
            self.best_avg_reward = avg_reward
            self.save_models("artifacts/models/first_fight/ppo_agent_best.pt")
            print("New best reward found! saving to ppo_agent_beset.pt...")

        if self.learn_step_counter % 2 == 0:
            print("Average Loss at Episode " + str(self.learn_step_counter) + ": " + str(avg_loss))
            print("Average Reward at Episode " + str(self.learn_step_counter) + ": " + str(avg_reward))

            self.graph_history()

        self.learn_step_counter += 1

    # def _compute_log_prob_lstm_batch(self, batch_stages, batch_states, batch_actions, h_initial, c_initial):
    #     """
    #     Compute log probs for a BATCH of SEQUENCES, using an initial hidden state for each sequence.
    #     This version is vectorized and much more efficient.
    #
    #     Args:
    #         batch_stages (Tensor): Shape (batch_size, sequence_length)
    #         batch_states (Tensor): Shape (batch_size, sequence_length, state_dim)
    #         batch_actions (Tensor): Shape (batch_size, sequence_length)
    #         h_initial (Tensor): Initial hidden state, shape (batch_size, 1, 1, hidden_dim)
    #         c_initial (Tensor): Initial cell state, shape (batch_size, 1, 1, hidden_dim)
    #     """
    #     # --- 1. Prepare Inputs and Hidden States ---
    #
    #     # Get batch dimensions
    #     episode_length, _ = batch_states.shape
    #
    #     # Reshape the initial hidden states to the format expected by the LSTM:
    #     # (num_layers, batch_size, hidden_dim)
    #     # The squeeze removes the dimensions of size 1, and transpose swaps episode and layer dims.
    #     initial_hidden_state = (h_initial, c_initial)
    #
    #     # Normalize observations during training (don't update stats, just use existing)
    #     # We normalize each observation in the batch
    #     features_normalized = torch.stack([
    #         self.obs_norm.normalize(batch_states[i], update=False)
    #         for i in range(batch_states.shape[0])
    #     ])
    #     features_normalized = features_normalized.unsqueeze(0)
    #
    #     # --- 2. Vectorized Forward Pass ---
    #
    #     # Process all battle sequences through the LSTM at once
    #     # The LSTM will process the tensor of shape (batch_size, self.embed_dim)
    #
    #     lstm_out, _ = self.actor_critic.lstm(features_normalized, initial_hidden_state)
    #
    #     # Combine LSTM output with static features
    #     bt_base_out = self.actor_critic.base_network(lstm_out)
    #
    #     # Process all card build sequences through the non-LSTM path
    #     cb_base_out = self.actor_critic.cb_base_network(features_normalized)
    #
    #     # Use a mask to select the correct output for each item in the batch based on its stage
    #
    #     # is_battle_stage = (batch_stages == self.GameStage.BATTLE.value).to(self.device).squeeze(-1)
    #     is_battle_stage = torch.tensor([stage == self.GameStage.BATTLE.value for stage in batch_stages]).to(self.device)
    #     base_output = torch.where(is_battle_stage.unsqueeze(-1), bt_base_out, cb_base_out).to(self.device)
    #
    #     # --- 3. Get Logits, Values, and Entropy ---
    #
    #     # Get values from the critic head
    #     values = self.actor_critic.critic_head(base_output).squeeze(-1)  # Shape: (batch_size, sequence_length)
    #
    #     # Get logits from the correct actor head using the same mask
    #     bt_logits = self.actor_critic.actor_bt_head(base_output)
    #     cb_logits = self.actor_critic.actor_cb_head(base_output)
    #
    #     # log_probs = torch.empty(batch_size, episode_length, device=self.device)
    #     # entropy = torch.empty(batch_size, episode_length, device=self.device)
    #     log_probs = torch.empty(episode_length, device=self.device)
    #     entropy = torch.empty(episode_length, device=self.device)
    #
    #     bt_mask = is_battle_stage
    #     if bt_mask.any():
    #         bt_dist = torch.distributions.Categorical(logits=bt_logits[bt_mask])
    #         log_probs[bt_mask] = bt_dist.log_prob(batch_actions[bt_mask])
    #         entropy[bt_mask] = bt_dist.entropy()
    #
    #     cb_mask = ~is_battle_stage
    #     if cb_mask.any():
    #         cb_dist = torch.distributions.Categorical(logits=cb_logits[cb_mask])
    #         log_probs[cb_mask] = cb_dist.log_prob(batch_actions[cb_mask])
    #         entropy[cb_mask] = cb_dist.entropy()
    #
    #     return log_probs, entropy, values

    def _compute_log_prob_lstm_batch(self, batch_stages, batch_states, batch_actions, h_initial, c_initial):
        """
        Recomputes log probabilities, entropy, and values for a single episode's worth of steps.
        Called during _learn() after batch_states has already been normalized and encoded.

        Args:
            batch_stages  : list of int, length (episode_len,)
                            Stage enum values (BATTLE=0, CARD_BUILD=1) for each step.
            batch_states  : Tensor, shape (episode_len, embed_dim)
                            Already-encoded, already-normalized state embeddings from state_encoder.
            batch_actions : Tensor, shape (episode_len,)
                            Actions taken during rollout, used to compute log probs.
            h_initial     : Tensor, shape (num_layers, 1, lstm_hidden_dim)
                            Initial LSTM hidden state — zeros for episode start.
            c_initial     : Tensor, shape (num_layers, 1, lstm_hidden_dim)
                            Initial LSTM cell state — zeros for episode start.

        Returns:
            log_probs : Tensor, shape (episode_len,)
            entropy   : Tensor, shape (episode_len,)
            values    : Tensor, shape (episode_len,)
        """
        episode_len, embed_dim = batch_states.shape
        # batch_states: (episode_len, embed_dim)

        # --- 1. LSTM forward pass — battle steps only ---
        # Card build steps must not update the hidden state (matches rollout behavior where
        # self.hidden_state is only updated for BATTLE stage).  We step through the episode
        # manually so we can skip LSTM updates for card build steps.
        h, c = h_initial, c_initial
        lstm_out = torch.zeros(episode_len, self.lstm_hidden_dim, device=self.device)
        for i, stage in enumerate(batch_stages):
            if stage == self.GameStage.BATTLE.value:
                step_in = batch_states[i].unsqueeze(0).unsqueeze(0)  # (1, 1, embed_dim)
                step_out, (h, c) = self.actor_critic.lstm(step_in, (h, c))
                lstm_out[i] = step_out.squeeze(0).squeeze(0)
        # lstm_out: (episode_len, lstm_hidden_dim)
        # Card build rows are zero — they are unused below (cb_base_network is used instead).

        # --- 2. Base network passes ---
        # Battle path: LSTM output → base_network
        bt_base_out = self.actor_critic.base_network(lstm_out)
        # bt_base_out: (episode_len, network_size // 2)

        # Card build path: raw embedding → cb_base_network (bypasses LSTM entirely)
        cb_base_out = self.actor_critic.cb_base_network(batch_states)
        # cb_base_out: (episode_len, network_size // 2)

        # --- 3. Select correct base output per step based on game stage ---
        is_battle_stage = torch.tensor(
            [stage == self.GameStage.BATTLE.value for stage in batch_stages],
            dtype=torch.bool, device=self.device
        )
        # is_battle_stage: (episode_len,)

        # Expand to match feature dim for torch.where broadcasting
        stage_mask = is_battle_stage.unsqueeze(-1).expand_as(bt_base_out)
        # stage_mask: (episode_len, network_size // 2)

        base_output = torch.where(stage_mask, bt_base_out, cb_base_out)
        # base_output: (episode_len, network_size // 2)

        # --- 4. Critic values ---
        values = self.actor_critic.critic_head(base_output).squeeze(-1)
        # critic_head output: (episode_len, 1) → squeeze → (episode_len,)

        # --- 5. Actor logits ---
        bt_logits = self.actor_critic.actor_bt_head(base_output)
        # bt_logits: (episode_len, total_bt_actions)

        cb_logits = self.actor_critic.actor_cb_head(base_output)
        # cb_logits: (episode_len, total_cb_actions)

        # --- 6. Compute log probs and entropy, routing each step to the correct head ---
        log_probs = torch.empty(episode_len, device=self.device)
        entropy = torch.empty(episode_len, device=self.device)

        bt_mask = is_battle_stage
        # bt_mask: (episode_len,) — True for battle steps
        if bt_mask.any():
            bt_dist = torch.distributions.Categorical(logits=bt_logits[bt_mask])
            log_probs[bt_mask] = bt_dist.log_prob(batch_actions[bt_mask])
            entropy[bt_mask] = bt_dist.entropy()

        cb_mask = ~is_battle_stage
        # cb_mask: (episode_len,) — True for card build steps
        if cb_mask.any():
            cb_dist = torch.distributions.Categorical(logits=cb_logits[cb_mask])
            log_probs[cb_mask] = cb_dist.log_prob(batch_actions[cb_mask])
            entropy[cb_mask] = cb_dist.entropy()

        return log_probs, entropy, values

    def step(self, prev_state, action_taken, log_prob, reward, done, new_state, value):
        """
        Take a step for all agents and potentially learn

        Args:
            prev_state: Previous state for agent
            action_taken: Previous action taken for agent
            log_prob: Log probability of taking that action
            reward: Reward for taking that action
            done: Done flag for agent
            new_state: Newly reached state for agent to take new action

        Returns:
            actions: Chosen actions for all agents
        """
        new_state_tensor = self._convert_state_to_tensors(new_state)
        prev_state_tensor = self._convert_state_to_tensors(prev_state)

        embedded_prev_state, prev_stage, action_mask = self.embed_state(prev_state_tensor)
        # embedded_new_state, action_mask, stage = self.embed_state(new_state_tensor)
        # Store experiences
        if self.learning_enabled:
            self.remember(prev_stage, embedded_prev_state, action_taken, reward, done, log_prob, value, self.hidden_state)

        # Sample actions
        if not done:
            action, new_log_prob, value, action_probs = self.choose_action(new_state_tensor)
        else:
            action = None
            new_log_prob = None
            value = None
            action_probs = None

        # Learn if enough experiences are collected
        if self.learning_enabled and len(self.memory['states']) >= self.learn_size:
            self._learn()

        return action, new_log_prob, value, action_probs

    def save_models(self, filepath):
        """Save all model weights and observation normalization statistics"""
        checkpoint = {
            'state_encoder': self.state_encoder.state_dict(),
            'actor_critic': self.actor_critic.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'obs_norms': {
                key: {'mean': rms.mean, 'var': rms.var, 'count': rms.count}
                for key, rms in self.obs_norms.items()
            },
        }
        torch.save(checkpoint, filepath)

    def load_models(self, filepath):
        """Load all model weights and observation normalization statistics"""
        checkpoint = torch.load(filepath, weights_only=False)
        self.state_encoder.load_state_dict(checkpoint['state_encoder'])
        self.actor_critic.load_state_dict(checkpoint['actor_critic'])
        self.old_network.load_state_dict(self.actor_critic.state_dict())
        self.optimizer.load_state_dict(checkpoint['optimizer'])

        if 'obs_norms' in checkpoint:
            for key, stats in checkpoint['obs_norms'].items():
                if key in self.obs_norms:
                    self.obs_norms[key].mean = stats['mean']
                    self.obs_norms[key].var = stats['var']
                    self.obs_norms[key].count = stats['count']

