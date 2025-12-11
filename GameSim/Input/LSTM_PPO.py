import math
import random
from enum import Enum

import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical
import torch.nn.functional as F
import torch.optim as optim

from GameSim.Input.PPO import PPOAgent


class ActorCriticLSTM(nn.Module):
    """
    An Actor-Critic network that uses an LSTM to process sequential battle states.
    """
    def __init__(self, static_input_dim, dynamic_input_dim, lstm_hidden_dim, total_bt_actions, total_cb_actions):
        super().__init__()

        # --- LSTM for Battle Stage ---
        # This layer processes the sequence of states within a battle.
        self.lstm_hidden_dim = lstm_hidden_dim
        self.lstm = nn.LSTM(
            input_size=dynamic_input_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=1,
            batch_first=True  # Important for handling single-item batches
        )

        # --- Shared Base Network ---
        # This network now processes the LSTM's output combined with static features (like the deck embedding).
        combined_feature_dim = lstm_hidden_dim + static_input_dim
        leaky_relu_slope = 0.02
        network_size = 256

        xavier_gain = nn.init.calculate_gain('leaky_relu', leaky_relu_slope)
        first_layer = nn.Linear(combined_feature_dim, network_size)
        nn.init.xavier_uniform_(first_layer.weight, gain=xavier_gain)
        second_layer = nn.Linear(network_size, network_size // 2)
        nn.init.xavier_uniform_(second_layer.weight, gain=xavier_gain)
        self.base_network = nn.Sequential(
            first_layer,
            # nn.LayerNorm(network_size),
            nn.LeakyReLU(leaky_relu_slope),
            second_layer,
            # nn.LayerNorm(network_size // 2),
            nn.LeakyReLU()
        )

        # --- Actor Heads ---
        self.actor_bt_head = nn.Linear(network_size // 2, total_bt_actions)
        nn.init.xavier_uniform_(self.actor_bt_head.weight, gain=xavier_gain)
        # The Card Build head does not use the LSTM, it uses a separate simple network.
        cb_layer = nn.Linear(static_input_dim, network_size // 2)
        nn.init.xavier_uniform_(cb_layer.weight, gain=xavier_gain)
        self.cb_base_network = nn.Sequential(
            cb_layer, # Only sees static deck/player info
            # nn.LayerNorm(network_size // 2),
            nn.LeakyReLU(leaky_relu_slope)
        )
        self.actor_cb_head = nn.Linear(network_size // 2, total_cb_actions)
        nn.init.xavier_uniform_(self.actor_cb_head.weight, gain=xavier_gain)

        # --- Critic Head ---
        self.critic_head = nn.Linear(network_size // 2, 1)
        nn.init.xavier_uniform_(self.critic_head.weight, gain=xavier_gain)

    def forward(self, static_features, dynamic_features, hidden_state, stage):
        """
        Performs a forward pass. Note the new 'hidden_state' argument.
        """
        if stage == PPOAgent.GameStage.BATTLE:
            # Pass dynamic features and the previous hidden state through the LSTM.
            # We add a sequence dimension (1) to the input tensor.
            # print(hidden_state[0].shape)
            # print(hidden_state[1].shape)
            dynamic_features = dynamic_features.unsqueeze(0).unsqueeze(0)
            # print(dynamic_features.shape)
            lstm_out, new_hidden_state = self.lstm(dynamic_features, hidden_state)

            # The output needs to be squeezed to remove the sequence dimension before concatenation.
            lstm_out = lstm_out.squeeze(0).squeeze(0)

            # Combine the LSTM's output with the static features (e.g., deck embedding).
            combined_features = torch.cat((lstm_out, static_features), dim=-1)

            # Pass the combined vector through the base network.
            base_output = self.base_network(combined_features)

        elif stage == PPOAgent.GameStage.CARD_BUILD:
            # Card building is not sequential, so we bypass the LSTM.
            # The new_hidden_state is None because we are not in a battle sequence.
            base_output = self.cb_base_network(static_features)
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

    def sample_action(self, stage, static_features, dynamic_features, hidden_state, action_mask):
        # --- Get Action Logits and State Value ---
        action_logits, state_value, new_hidden_state = self.forward(static_features, dynamic_features, hidden_state, stage)

        masked_logits = action_logits.clone()  # Use clone to avoid in-place modification issues
        masked_logits[~action_mask] = -1e9

        # --- Sample Action ---
        action_dist = Categorical(logits=masked_logits)
        action = action_dist.sample()
        # print(action_dist.probs)
        #
        log_prob = action_dist.log_prob(action).unsqueeze(-1)

        return action, log_prob, state_value, new_hidden_state

class LSTMPPOAgent(PPOAgent):
    # class GameStage(Enum):
    #     BATTLE = 0
    #     CARD_BUILD = 1

    def __init__(self, num_actions, card_feature_length, player_feature_length, enemy_feature_length, filepath, learning_enabled=True):
        super().__init__(num_actions, card_feature_length, enemy_feature_length, filepath, learning_enabled=learning_enabled)# (Keep your existing __init__ arguments)

        self.best_avg_reward = -math.inf
        # Define the dimensions for the new network
        self.lstm_hidden_dim = 256
        # Static features are things that don't change turn-to-turn (like the deck)
        static_dim = self.card_embed_dim
        # Dynamic features are turn-specific (player stats, hand, enemies)
        dynamic_dim = player_feature_length + (self.card_embed_dim * self.max_cards) + (self.max_enemies * self.enemy_embed_dim)

        # --- Initialize the New Network ---
        self.actor_critic = ActorCriticLSTM(
            static_input_dim=static_dim,
            dynamic_input_dim=dynamic_dim,
            lstm_hidden_dim=self.lstm_hidden_dim,
            total_bt_actions=(self.max_cards * self.max_enemies) + self.other_actions,
            total_cb_actions=self.max_card_choices
        )

        self.old_network = ActorCriticLSTM(
            static_input_dim=static_dim,
            dynamic_input_dim=dynamic_dim,
            lstm_hidden_dim=self.lstm_hidden_dim,
            total_bt_actions=(self.max_cards * self.max_enemies) + self.other_actions,
            total_cb_actions=self.max_card_choices
        )

        self.old_network.load_state_dict(self.actor_critic.state_dict())

        self.params = list(self.actor_critic.parameters()) + list(self.card_embedding.parameters())
        self.optimizer = optim.Adam(self.params, lr=self.lr)
        self.initial_lr = self.lr
        # self.lr_scheduler = optim.lr_scheduler.CyclicLR(self.optimizer,
        #                                                 self.initial_lr / 5,
        #                                                 self.initial_lr * 2,
        #                                                 step_size_up=100)

        self.lr_scheduler = optim.lr_scheduler.LinearLR(self.optimizer,
                                                        start_factor=self.initial_lr,
                                                        end_factor=self.initial_lr * 0.1,
                                                        total_iters=2000)

        # --- Add a placeholder for the hidden state ---
        self.hidden_state = None

        self.memory['hidden_states'] = []
        self.memory['cell_states'] = []

        self.sequence_length = 64

    def reset_hidden_state(self):
        """Call this at the beginning of each battle."""
        # Initialize a zero hidden state and cell state for the LSTM
        self.hidden_state = (
            torch.zeros(1, 1, self.lstm_hidden_dim).to(self.device),
            torch.zeros(1, 1, self.lstm_hidden_dim).to(self.device)
        )

    def remember(self, stage, state, action, reward, done, log_prob, value, hidden_state):
        """Override the remember method to also store the hidden state."""
        super().remember(stage, state, action, reward, done, log_prob, value)

        # Unpack and store the hidden and cell states
        h, c = hidden_state
        self.memory['hidden_states'].append(h.detach().cpu().numpy())
        self.memory['cell_states'].append(c.detach().cpu().numpy())

    def choose_action(self, state_tensors):
        """Choose action, now passing the hidden state."""
        # --- You will need to modify embed_state to return static and dynamic features separately ---
        # For now, let's assume it does:
        # static_features, dynamic_features, stage, action_mask = self.embed_state_v2(state_tensors)

        full_state, stage, action_mask = self.embed_state(state_tensors)
        static_features = full_state[:self.card_embed_dim]
        dynamic_features = full_state[self.card_embed_dim:]

        self.actor_critic.eval()
        with torch.no_grad():
            # Pass the current hidden state to the network
            action_choice, log_prob, value, new_hidden_state = self.actor_critic.sample_action(
                stage, static_features, dynamic_features, self.hidden_state, action_mask
            )
            # Update the agent's hidden state for the next step
            if stage == self.GameStage.BATTLE:
                self.hidden_state = new_hidden_state

        self.actor_critic.train()
        return action_choice, log_prob, value

    def _learn(self):
        # self.device = "mps"
        # --- Retrieve all data from memory ---
        states_arr = np.array(self.memory['states'])
        actions_arr = np.array(self.memory['actions'])
        rewards_arr = np.array(self.memory['rewards'])
        dones_arr = np.array(self.memory['dones'])
        old_log_probs_arr = np.array(self.memory['log_probs'])
        values_arr = np.array(self.memory['values'])
        stages_arr = np.array(self.memory['stages'])
        # hidden_states_arr = np.array(self.memory['hidden_states'])
        # cell_states_arr = np.array(self.memory['cell_states'])

        advantages_arr = self._compute_gae(rewards_arr, values_arr, dones_arr)
        advantages = torch.tensor(advantages_arr, dtype=torch.float32).to(self.device)
        advantages_all = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        value_targets_all = advantages_all + torch.tensor(values_arr, dtype=torch.float32).to(self.device)

        episode_indices = []
        current_episode_start = 0
        # Find the start index of each episode
        for i in range(len(dones_arr)):
            if dones_arr[i]:
                episode_indices.append(range(current_episode_start, i + 1))
                current_episode_start = i + 1

        losses = []
        for _ in range(self.learn_epochs):
            # Shuffle the sequences, NOT the individual steps
            random.shuffle(episode_indices)

            for episode in episode_indices:
                episode_len = len(episode)
                if episode_len == 0:
                    continue

                # Get the mini-batch of sequences
                batch_states = torch.tensor(states_arr[episode], dtype=torch.float32).to(self.device)
                batch_actions = torch.tensor(actions_arr[episode], dtype=torch.long).to(self.device)
                batch_old_log_probs = torch.tensor(old_log_probs_arr[episode], dtype=torch.float32).to(
                    self.device)
                batch_advantages = advantages_all[episode].to(self.device)
                batch_value_targets = value_targets_all[episode].to(self.device)
                batch_stages = stages_arr[episode]
                initial_hidden_state = (
                    torch.zeros(1, self.lstm_hidden_dim).to(self.device),
                    torch.zeros(1, self.lstm_hidden_dim).to(self.device)
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
                self.optimizer.step()

            self.lr_scheduler.step()
            self.entropy_coef *= self.entropy_decay
            self.learn_step_counter += 1

        self.old_network.load_state_dict(self.actor_critic.state_dict())
        # Clear memory after learning
        for key in self.memory:
            self.memory[key].clear()

        if self.learn_step_counter % 10 == 0:
            avg_loss = sum(losses) / len(losses)
            avg_reward = (sum(rewards_arr) / len(rewards_arr))
            print("Average Loss at Episode " + str(self.learn_step_counter) + ": " + str(avg_loss))
            print("Average Reward at Episode " + str(self.learn_step_counter) + ": " + str(avg_reward))
            print(f"Current paramters: entropy_coef={self.entropy_coef} ")
            self.losses.append(avg_loss)
            self.rewards.append(avg_reward)

            if avg_reward > self.best_avg_reward:
                self.best_avg_reward = avg_reward
                self.save_models("artifacts/models/first_fight/ppo_agent_best.pt")
                print("New best reward found! saving to ppo_agent_beset.pt...")

        if self.learn_step_counter % 50 == 0:
            self.graph_history()
        # self.device = "cpu"

    def _compute_log_prob_lstm_batch(self, batch_stages, batch_states, batch_actions, h_initial, c_initial):
        """
        Compute log probs for a BATCH of SEQUENCES, using an initial hidden state for each sequence.
        This version is vectorized and much more efficient.

        Args:
            batch_stages (Tensor): Shape (batch_size, sequence_length)
            batch_states (Tensor): Shape (batch_size, sequence_length, state_dim)
            batch_actions (Tensor): Shape (batch_size, sequence_length)
            h_initial (Tensor): Initial hidden state, shape (batch_size, 1, 1, hidden_dim)
            c_initial (Tensor): Initial cell state, shape (batch_size, 1, 1, hidden_dim)
        """
        # --- 1. Prepare Inputs and Hidden States ---

        # Get batch dimensions
        episode_length, _ = batch_states.shape
        # batch_size, episode_length, _ = batch_states.shape

        # Reshape the initial hidden states to the format expected by the LSTM:
        # (num_layers, batch_size, hidden_dim)
        # The squeeze removes the dimensions of size 1, and transpose swaps episode and layer dims.
        # h_0 = h_initial.squeeze(1).transpose(0, 1)
        # c_0 = c_initial.squeeze(1).transpose(0, 1)
        # print(h_initial.shape)
        initial_hidden_state = (h_initial, c_initial)

        # Separate state into static and dynamic parts for the model across the whole batch
        # static_features = batch_states[:, :, :self.card_embed_dim]
        # dynamic_features = batch_states[:, :, self.card_embed_dim:]
        static_features = batch_states[:, :self.card_embed_dim]
        dynamic_features = batch_states[:, self.card_embed_dim:]

        # --- 2. Vectorized Forward Pass ---

        # Process all battle sequences through the LSTM at once
        # The LSTM will process the tensor of shape (batch_size, sequence_length, dynamic_dim)

        lstm_out, _ = self.actor_critic.lstm(dynamic_features, initial_hidden_state)

        # Combine LSTM output with static features
        combined_features = torch.cat((lstm_out, static_features), dim=-1)
        bt_base_out = self.actor_critic.base_network(combined_features)

        # Process all card build sequences through the non-LSTM path
        cb_base_out = self.actor_critic.cb_base_network(static_features)

        # Use a mask to select the correct output for each item in the batch based on its stage

        # is_battle_stage = (batch_stages == self.GameStage.BATTLE.value).to(self.device).squeeze(-1)
        is_battle_stage = torch.tensor((batch_stages == self.GameStage.BATTLE.value)).to(self.device)
        base_output = torch.where(is_battle_stage.unsqueeze(-1), bt_base_out, cb_base_out).to(self.device)

        # --- 3. Get Logits, Values, and Entropy ---

        # Get values from the critic head
        values = self.actor_critic.critic_head(base_output).squeeze(-1)  # Shape: (batch_size, sequence_length)

        # Get logits from the correct actor head using the same mask
        bt_logits = self.actor_critic.actor_bt_head(base_output)
        cb_logits = self.actor_critic.actor_cb_head(base_output)

        # log_probs = torch.empty(batch_size, episode_length, device=self.device)
        # entropy = torch.empty(batch_size, episode_length, device=self.device)
        log_probs = torch.empty(episode_length, device=self.device)
        entropy = torch.empty(episode_length, device=self.device)

        bt_mask = is_battle_stage
        if bt_mask.any():
            bt_dist = torch.distributions.Categorical(logits=bt_logits[bt_mask])
            log_probs[bt_mask] = bt_dist.log_prob(batch_actions[bt_mask])
            entropy[bt_mask] = bt_dist.entropy()

        cb_mask = ~is_battle_stage
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
            action, new_log_prob, value = self.choose_action(new_state_tensor)
        else:
            action = None
            new_log_prob = None
            value = None

        # Learn if enough experiences are collected
        if self.learning_enabled and len(self.memory['states']) >= self.learn_size:
            self._learn()

        return action, new_log_prob, value

