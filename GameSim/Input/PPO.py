from enum import Enum
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from CombatSim.util import visualize_bot_history, visualize_embeddings


class ActorCritic(nn.Module):
    """
    A unified Actor-Critic network that shares a base feature extractor.
    """

    def __init__(self, embedded_state_dim, total_bt_actions, total_cb_actions):
        super().__init__()

        # Shared base network
        self.base_network = nn.Sequential(
            nn.Linear(embedded_state_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU()
        )

        # --- Actor Heads ---
        self.actor_bt_head = nn.Linear(128, total_bt_actions)
        self.actor_cb_head = nn.Linear(128, total_cb_actions)

        # --- Critic Head ---
        # Outputs a single value for the state
        self.critic_head = nn.Linear(128, 1)

    def forward(self, embedded_state, stage):
        """
        Performs a forward pass through the network.

        Returns:
            tuple: A tuple containing (action_logits, state_value).
        """
        # Pass state through the shared base
        base_output = self.base_network(embedded_state)

        # Get the state value from the critic head
        state_value = self.critic_head(base_output)

        # Get action logits from the appropriate actor head
        if stage == PPOAgent.GameStage.BATTLE:
            action_logits = self.actor_bt_head(base_output)
        elif stage == PPOAgent.GameStage.CARD_BUILD:
            action_logits = self.actor_cb_head(base_output)
        else:
            raise ValueError(f"Unknown stage: {stage}")

        return action_logits, state_value.squeeze(-1)  # Squeeze to remove trailing dim

    def sample_action(self, stage, embedded_state, action_mask):

        # Compute action logits
        action_logits, value = self.forward(embedded_state, stage)

        # Apply the action mask
        # We set the logits of illegal actions to a very large negative number.
        # This makes their probability effectively zero after the softmax.
        masked_logits = action_logits.clone()  # Use clone to avoid in-place modification issues
        masked_logits[~action_mask] = -1e9

        # Create categorical distribution
        dist = torch.distributions.Categorical(logits=masked_logits)
        # print("action distribution:")
        # print(dist.probs)
        # Sample action
        action = dist.sample()

        # Compute log probability of the sampled action
        log_prob = dist.log_prob(action).unsqueeze(-1)

        return action, log_prob, value, dist.probs


class CardEncoder(nn.Module):
    """
    A neural network to encode a vector of card features into a dense embedding.
    """

    def __init__(self, feature_vector_dim: int, embedding_dim: int):
        """
        Args:
            feature_vector_dim (int): The size of the input card feature vector.
            embedding_dim (int): The desired size of the output card embedding.
        """
        super().__init__()

        # A sequence of layers forming a Multi-Layer Perceptron (MLP).
        # We use Linear layers with a non-linear activation (ReLU) in between.
        leaky_relu_slope = 0.02
        network_size = 256
        xavier_gain = nn.init.calculate_gain('leaky_relu', leaky_relu_slope)
        layer_1 = nn.Linear(feature_vector_dim, network_size)
        nn.init.xavier_uniform_(layer_1.weight, gain=xavier_gain)
        layer_2 = nn.Linear(network_size, network_size // 2)
        nn.init.xavier_uniform_(layer_2.weight, gain=xavier_gain)
        layer_3 = nn.Linear(network_size // 2, embedding_dim)
        nn.init.xavier_uniform_(layer_3.weight, gain=xavier_gain)
        self.network = nn.Sequential(
            layer_1,
            # nn.LayerNorm(network_size),
            nn.LeakyReLU(leaky_relu_slope),
            layer_2,
            # nn.LayerNorm(network_size // 2), # do these before each non-linear function
            nn.LeakyReLU(leaky_relu_slope),
            layer_3
        )

    def forward(self, card_features_batch: torch.Tensor) -> torch.Tensor:
        """
        Performs the forward pass to generate embeddings.

        Args:
            card_features_batch (torch.Tensor): A tensor of card features.
                                                Shape: (batch_size, feature_vector_dim)

        Returns:
            torch.Tensor: The resulting card embeddings.
                           Shape: (batch_size, embedding_dim)
        """
        return self.network(card_features_batch)

class PPOAgent:
    class GameStage(Enum):
        BATTLE = 0
        CARD_BUILD = 1

    # def __init__(self, num_actions, card_feature_length, enemy_feature_length, filepath, embedding_dim=256, learning_enabled=True, lr=0.0005,
    #              gamma=0.99, epsilon=0.2, value_coef=0.5, entropy_coef=0.001, entropy_decay=0.99, learn_epochs=5):
    def __init__(self, num_actions, card_feature_length, enemy_feature_length, filepath, embedding_dim=128,
                 learning_enabled=True, lr=0.001, gamma=0.99, epsilon=0.23, value_coef=0.5, entropy_coef=0.0005, entropy_decay=0.999, learn_epochs=10):

        # Hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        self.entropy_decay = entropy_decay
        self.learn_epochs = learn_epochs
        self.learning_enabled = learning_enabled
        self.lr = lr

        self.filepath = filepath

        # Device configuration
        self.device = torch.device(
            "mps" if torch.backends.mps.is_available() else
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        # self.device = torch.device("cpu")
        print(f"Using device: {self.device}")

        # Card Embeddings
        self.card_embed_dim = embedding_dim
        self.card_embedding = CardEncoder(card_feature_length, embedding_dim).to(self.device)

        self.enemy_embed_dim = enemy_feature_length

        self.max_cards, self.max_enemies, self.other_actions = num_actions["BT"]
        self.max_card_choices = num_actions["CB"]

        # Initialize actors and critics for each agent
        self.state_dim = self.card_embed_dim + (self.card_embed_dim * self.max_cards)
        self.state_dim += self.max_enemies * self.enemy_embed_dim + 13  # 13 Player features
        self.actor_critic = ActorCritic(self.state_dim, (self.max_cards * self.max_enemies) + self.other_actions, self.max_card_choices).to(self.device)
        self.old_network = ActorCritic(self.state_dim, (self.max_cards * self.max_enemies) + self.other_actions, self.max_card_choices).to(self.device)
        # self.actor_critic = ActorCritic(self.state_dim, self.card_embed_dim, self.enemy_embed_dim, self.max_card_choices).to(self.device)
        #
        # self.old_network = ActorCritic(self.state_dim, self.card_embed_dim, self.enemy_embed_dim, self.max_card_choices).to(self.device)

        self.old_network.load_state_dict(self.actor_critic.state_dict())

        # Optimizers
        params = list(self.actor_critic.parameters()) + list(self.card_embedding.parameters())
        self.optimizer = optim.Adam(params, lr=lr)
        self.initial_lr = lr
        self.lr_scheduler = optim.lr_scheduler.LinearLR(
            self.optimizer,
            start_factor=1.0,
            end_factor=0.05,
            total_iters=2_500
        )


        # Memory parameters
        self.memory = {
            'states': [],
            # 'hand_embeds': [],
            # 'enemy_features': [],
            # 'choice_embeds': [],
            'actions': [],
            'rewards': [],
            'dones': [],
            'log_probs': [],
            'values': [],
            'stages': [],
            # 'action_masks': []
        }
        self.batch_size = 1024
        self.learn_size = 8192
        self.max_memory = 20000

        self.learn_step_counter = 0

        # Use deque with maxlen to prevent unbounded memory growth
        self.max_history = 1000  # Keep last 1000 entries
        self.losses = deque(maxlen=self.max_history)
        self.rewards = deque(maxlen=self.max_history)

    def reset_hidden_state(self):
        pass

    def remember(self, stage, state, action, reward, done, log_prob, value):
        """Store experience for multiple agents"""

        self.memory['states'].append(state.detach().cpu().numpy())
        # self.memory['hand_embeds'].append(hand_embed.detach().cpu().numpy())
        # self.memory['choice_embeds'].append(choice_embed.detach().cpu().numpy())
        # self.memory['enemy_features'].append(enemy_features)
        # self.memory['action_masks'].append(action_mask)

        # For simple objects, store them directly
        self.memory['stages'].append(stage.value)
        self.memory['rewards'].append(reward)
        self.memory['dones'].append(done)

        # For scalar tensors, use .item() to get the Python number
        self.memory['actions'].append(action.item() if isinstance(action, torch.Tensor) else action)
        self.memory['log_probs'].append(log_prob.item())
        self.memory['values'].append(value.item())

        # Trim memory if exceeds max size
        if len(self.memory['states']) > self.max_memory:
            for key in self.memory:
                self.memory[key].pop(0)

    def embed_state(self, state):
        """
        Embeds the raw state dictionary into a single flat tensor for the actor/critic.

        Args:
            state (dict): A dictionary with 'deck' 'player' 'card_choices'.
                          - state['deck']: A tensor of card feature vectors.
                                           Shape: (num_cards_in_deck, card_feature_vector_dim)
                          - state['features']: A flat tensor of other game state features.

        Returns:
            tuple: A tuple containing the state_tensor, action_mask, current game stage, hand_embeddings, enemy_features, and card_choice embeddings
        """
        # Note: The input 'deck' should be the tensor of raw feature vectors, not embeddings yet.

        # Grab features which are guaranteed to be in the state dictionary.
        deck_card_features = state['deck'].to(self.device)
        player = state['player'].to(self.device)

        # Handle the edge case where the deck is empty
        if deck_card_features.shape[0] == 0:
            # If there are no cards, the deck's representation is just a zero vector.
            deck_embed = torch.zeros(self.card_embed_dim, device=self.device)
        else:
            # 1. Get embeddings for all cards in the deck.
            #    The CardEncoder handles the transformation from features to embeddings.
            #    Input shape: (num_cards_in_deck, feature_dim)
            #    Output shape: (num_cards_in_deck, card_embed_dim)
            deck_card_embeddings = torch.tensor(np.array([0 for i in range(self.card_embed_dim)]), device=self.device)
            deck_card_embeddings = self.card_embedding(deck_card_features)

            # 2. Aggregate the embeddings into a single vector using mean.
            #    We average across dimension 0 (the list of cards).
            #    This will always result in a tensor of shape (card_embed_dim,).
            deck_embed = torch.mean(deck_card_embeddings, dim=0)

        # hand_embeddings = None
        # enemies_embeddings = None

        # Now we will deal with features which may or may not be in the state dict depending on game stage.
        if 'card_choices' in state.keys():
            stage = self.GameStage.CARD_BUILD
            choices_embed = state['card_choices'].to(self.device)
            choices_embed = self.card_embedding(choices_embed)
            choices_embed = torch.flatten(choices_embed)

            # hand_embed = torch.zeros(self.card_embed_dim, device=self.device)
            hand_embed = torch.zeros((self.max_cards, self.card_embed_dim), device=self.device).flatten()
            enemies_embed = torch.zeros((self.max_enemies * self.enemy_embed_dim))
        else:
            stage = self.GameStage.BATTLE
            choices_embed = torch.zeros((self.max_card_choices, self.card_embed_dim), device=self.device).flatten()
            enemies_embed = state['enemies']

            hand_card_features = state['hand'].to(self.device)
            num_cards_in_hand = hand_card_features.shape[0]

            if enemies_embed.shape[0] == 0:
                enemies_embed = torch.zeros(self.max_enemies * self.enemy_embed_dim, device=self.device)
                # enemies_embeddings = None
            else:
                padding_needed = self.max_enemies - enemies_embed.shape[0]

                padded_enemy_embeddings = F.pad(enemies_embed, (0, 0, 0, padding_needed), "constant", 0)

                # Flatten the final (max_cards, card_embed_dim) tensor into a single vector
                enemies_embed = padded_enemy_embeddings.flatten()
                # enemies_embed = torch.mean(enemies_embeddings, dim=0)
            if num_cards_in_hand == 0:
                # If hand is empty, create a zero tensor for the full hand embedding size
                hand_embed = torch.zeros(self.max_cards * self.card_embed_dim, device=self.device)
            else:
                # Get embeddings for the cards currently in hand
                hand_embeddings = self.card_embedding(hand_card_features)  # Shape: (num_cards_in_hand, embed_dim)
                # Calculate how many empty card slots to pad
                padding_needed = self.max_cards - num_cards_in_hand

                # Pad the tensor with zeros to reach the max_cards length.
                # The padding format is (pad_left, pad_right, pad_top, pad_bottom).
                # We only pad the "bottom" of the card list dimension (dim 0).
                padded_hand_embeddings = F.pad(hand_embeddings, (0, 0, 0, padding_needed), "constant", 0)

                # Flatten the final (max_cards, card_embed_dim) tensor into a single vector
                hand_embed = padded_hand_embeddings.flatten()
                # hand_embed = torch.mean(hand_embeddings, dim=0)

        # 3. Concatenate the single deck embedding vector with the other state features.
        return (torch.cat((deck_embed, player, hand_embed, enemies_embed)), stage, state['action_mask'])

    def choose_action(self, state_tensors):
        """Choose actions for agent"""
        # if isinstance(state, dict):
        # state = self._convert_state_to_tensors(state)
        state, stage, action_mask = self.embed_state(state_tensors)

        # state = state.unsqueeze(0)

        self.actor_critic.eval()
        with torch.no_grad():
            agent_action, agent_log_prob, value, action_probs = self.actor_critic.sample_action(stage, state, action_mask)

        self.actor_critic.train()

        return agent_action, agent_log_prob, value, action_probs

    def _compute_gae(self, rewards, values, dones, lambda_=0.95):
        """Compute Generalized Advantage Estimation"""
        advantages = []
        gae = 0

        # add terminating value
        values = np.append(values, 0)

        # Reverse iteration
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + self.gamma * values[t + 1] * (1 - dones[t]) - values[t]
            gae = delta + self.gamma * lambda_ * (1 - dones[t]) * gae
            advantages.insert(0, gae)

        return advantages

    def _compute_vanilla_pg_advantage(self, rewards, values, dones):
        """
        Compute Vanilla Policy Gradient Advantage Estimation

        Unlike GAE, this method uses a simpler advantage calculation
        based on the difference between rewards and estimated values.

        Args:
            rewards (np.array): Rewards for each time step
            values (np.array): Estimated state values
            dones (np.array): Episode termination flags
            gamma (float): Discount factor

        Returns:
            np.array: Advantages calculated using vanilla policy gradient method
        """
        advantages = []

        # Compute advantages for each time step
        for t in range(len(rewards)):
            # Compute the discounted return
            discounted_return = 0
            for j in range(t, len(rewards)):
                if dones[j]:
                    break
                # Accumulate discounted rewards
                discounted_return += (self.gamma ** (j - t)) * rewards[j]

            # Subtract the estimated value of the current state
            advantage = discounted_return - values[t]
            advantages.append(advantage)

        return advantages

    def _learn(self):
        # 1. Retrieve all data from memory for this learning phase
        states_arr = np.array(self.memory['states'])
        # hands_arr = np.array(self.memory['hand_embeds'])
        # enemies_arr = np.array(self.memory['enemy_features'])
        # card_choice_arr = np.array(self.memory['choice_embeds'])
        actions_arr = np.array(self.memory['actions'])
        rewards_arr = np.array(self.memory['rewards'])
        dones_arr = np.array(self.memory['dones'])
        old_log_probs_arr = np.array(self.memory['log_probs'])
        values_arr = np.array(self.memory['values'])
        stages_arr = np.array(self.memory['stages'])

        # 2. Calculate advantages ONCE using the full set of trajectories
        advantages_arr = self._compute_gae(rewards_arr, values_arr, dones_arr)
        # advantages_arr = self._compute_vanilla_pg_advantage(rewards_arr, values_arr, dones_arr)
        advantages = torch.tensor(advantages_arr, dtype=torch.float32).to(self.device)
        advantages_all = (advantages - advantages.mean()) / (advantages.std() + 1e-8)  # Normalize advantages

        # Also calculate the value targets here
        value_targets_all = advantages_all + torch.tensor(values_arr, dtype=torch.float32).to(self.device)

        # values = self.update_critic()
        num_batches = self.learn_size // self.batch_size
        losses = []
        for i in range(self.learn_epochs):
            indices = np.arange(self.learn_size)
            np.random.shuffle(indices)

            for batch in range(1, num_batches):
                start_batch = (batch-1) * self.batch_size
                end_batch = batch * self.batch_size

                batch_indices = indices[start_batch:end_batch]

                states = torch.tensor(states_arr[batch_indices]).to(self.device)
                # max_cards_in_batch = 0
                # for i in batch_indices:
                #     if self.memory['hand_embeds'][i] is not None:
                #         max_cards_in_batch = max(max_cards_in_batch, self.memory['hand_embeds'][i].shape[0])
                #
                # # 2. Create the padded batch tensor
                # hand_batch = torch.zeros(self.batch_size, max_cards_in_batch, self.card_embed_dim)
                # for i, mem_idx in enumerate(batch_indices):
                #     hand_embed = self.memory['hand_embeds'][mem_idx]
                #     if hand_embed is not None:
                #         num_cards = hand_embed.shape[0]
                #         hand_batch[i, :num_cards, :] = torch.from_numpy(hand_embed)
                #
                # hands = hand_batch.to(self.device)
                # enemies = torch.tensor(enemies_arr[batch_indices]).to(self.device)
                # card_choices = torch.tensor(card_choice_arr[batch_indices]).to(self.device)
                actions = torch.tensor(actions_arr[batch_indices], dtype=torch.long).to(self.device)
                old_log_probs = torch.tensor(old_log_probs_arr[batch_indices], dtype=torch.float32).to(self.device)
                stages = torch.tensor(stages_arr[batch_indices],dtype=torch.float32).to(self.device)
                advantages = advantages_all[batch_indices]
                value_targets = value_targets_all[batch_indices]

                """Update network weights using PPO"""

                # Recompute log probabilities
                # new_logits, new_values = self.actor_critic(states)
                new_log_prob, new_entropy, values = self._compute_log_prob(stages, states, actions)

                # Compute PPO loss
                # ratios = torch.exp(new_log_prob - old_log_probs)
                # surr1 = ratios * advantages
                # surr2 = torch.clamp(ratios, 1 - self.epsilon, 1 + self.epsilon) * advantages
                # policy_loss = -torch.min(surr1, surr2).mean()

                # Compute SPO loss
                ratios = torch.exp(new_log_prob - old_log_probs)
                objective = ratios * advantages
                penalty = (torch.abs(advantages) / (2 * self.epsilon)) * ((ratios - 1)**2)
                policy_loss = -torch.mean(objective - penalty)

                # Value Loss
                value_loss = F.mse_loss(values.squeeze(), value_targets)

                # Entropy loss
                entropy_loss = -new_entropy.mean()

                # Total loss
                actor_loss = (policy_loss +
                              self.value_coef * value_loss +
                              self.entropy_coef * entropy_loss
                              )

                losses.append(actor_loss)

                # Update actor
                self.optimizer.zero_grad()

                actor_loss.backward()

                # Gradient clipping
                # if self.learn_step_counter > 1000:
                #     torch.nn.utils.clip_grad_norm_(self.actors[agent_idx].parameters(), max_norm=0.5)

                self.optimizer.step()
            self.lr_scheduler.step()
            self.learn_step_counter += 1
            self.entropy_coef *= self.entropy_decay

        self.old_network.load_state_dict(self.actor_critic.state_dict())


        # Clear memory after learning
        for key in self.memory:
            self.memory[key].clear()

        if self.learn_step_counter % 10 == 0:
            avg_loss = (sum(losses) / len(losses)).item()
            avg_reward = (sum(rewards_arr) / len(rewards_arr))
            print("Average Loss at Episode " + str(self.learn_step_counter) + ": " + str(avg_loss))
            print("Average Reward at Episode " + str(self.learn_step_counter) + ": " + str(avg_reward))
            print(f"Current paramters: entropy_coef={self.entropy_coef} ")
            self.losses.append(avg_loss)
            self.rewards.append(avg_reward)

            if self.learn_step_counter % 50 == 0:
                self.graph_history()

    def graph_history(self):
        visualize_bot_history(self.losses, self.rewards, self.filepath + "rew_loss.png")

    def graph_embeddings(self, card_names, card_vectors):
        self.card_embedding.eval()
        card_vectors = torch.tensor(np.array(card_vectors)).to(self.device)
        embeddings = self.card_embedding(card_vectors).detach().cpu().numpy()
        visualize_embeddings(card_names, embeddings)
        self.card_embedding.train()

    def _compute_log_prob(self, stages, states, actions):
        """Compute log probabilities and entropy for an agent"""
        all_log_probs = []
        all_entropies = []
        all_values = []

        # Loop through each item in the batch
        for i in range(states.shape[0]):
            state = states[i]
            # Convert the stage value (0.0 or 1.0) back to an Enum
            stage_enum = self.GameStage(int(stages[i].item()))
            action = actions[i]

            # Get logits and value for the single state
            logits, value = self.actor_critic.forward(state, stage_enum)

            # Calculate log_prob and entropy for this single step
            dist = torch.distributions.Categorical(logits=logits)
            log_prob = dist.log_prob(action)
            entropy = dist.entropy()

            all_log_probs.append(log_prob)
            all_entropies.append(entropy)
            all_values.append(value)

        # Stack the results from the loop back into tensors
        return torch.stack(all_log_probs), torch.stack(all_entropies), torch.stack(all_values)

    def _convert_state_to_tensors(self, state_np: dict) -> dict:
        """
        Converts a state dictionary of NumPy arrays to a dictionary of PyTorch tensors.

        Args:
            state_np (dict): The state dictionary from the game simulation.
                             - state_np['deck']: NumPy array of card features.
                             - state_np['features']: NumPy array of other game features.

        Returns:
            dict: A new state dictionary with values as PyTorch tensors on the correct device.
        """
        # Use torch.tensor() instead of torch.from_numpy() to create a COPY
        # This breaks the reference to the numpy array, allowing it to be garbage collected
        # torch.from_numpy() shares memory and keeps the numpy array alive
        tensors = {}
        for key, value in state_np.items():
            if key == "action_mask":
                tensors[key] = torch.tensor(value, dtype=torch.bool, device=self.device)
                continue
            tensors[key] = torch.tensor(value, dtype=torch.float32, device=self.device)
        return tensors

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
            self.remember(prev_stage, embedded_prev_state, action_taken, reward, done, log_prob, value)

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
        """Save all model weights"""
        checkpoint = {
            'card_embedding': self.card_embedding.state_dict(),
            'actor_critic': self.actor_critic.state_dict(),
            'optimizer': self.optimizer.state_dict(),
        }
        torch.save(checkpoint, filepath)

    def load_models(self, filepath):
        """Load all model weights"""
        checkpoint = torch.load(filepath)
        self.card_embedding.load_state_dict(checkpoint['card_embedding'])
        self.actor_critic.load_state_dict(checkpoint['actor_critic'])
        self.old_network.load_state_dict(self.actor_critic.state_dict())
        self.optimizer.load_state_dict(checkpoint['optimizer'])
