from enum import Enum

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


# class Actor(nn.Module):
#     def __init__(self, num_inputs, num_possible_actions, num_neurons=128):
#         super(Actor, self).__init__()
#
#         self.layer_1 = nn.Linear(num_inputs, 256)
#         self.layer_2 = nn.Linear(256, 128)
#         self.layer_3 = nn.Linear(128, 64)
#         self.action_head = nn.Linear(64, num_possible_actions)
#
#     def forward(self, state):
#         x = F.relu(self.layer_1(state))
#         x = F.relu(self.layer_2(x))
#         x = F.relu(self.layer_3(x))
#
#         # Compute action logits
#         action_logits = self.action_head(x)
#
#         return action_logits
#
#     def sample_action(self, state):
#         # Compute action logits
#         action_logits = self.forward(state)
#
#         # Create categorical distribution
#         dist = torch.distributions.Categorical(logits=action_logits)
#
#         # Sample action
#         action = dist.sample()
#
#         # Compute log probability of the sampled action
#         log_prob = dist.log_prob(action).unsqueeze(-1)
#
#         return action, log_prob, action_logits
#
#
# class Critic(nn.Module):
#     def __init__(self, state_dim, num_neurons=128):
#         super(Critic, self).__init__()
#
#         # Total input will be: (96 observations)
#         total_input_dim = state_dim
#
#         self.layer_1 = nn.Linear(total_input_dim, 256)
#         self.layer_2 = nn.Linear(256, 128)
#         self.layer_3 = nn.Linear(128, 64)
#         self.value = nn.Linear(64, 1)
#
#     def forward(self, states):
#         x = states[:, 0]
#
#         # Concatenate all observations and actions
#         # x = torch.cat([states], dim=-1)
#
#         x = F.relu(self.layer_1(x))
#         x = F.relu(self.layer_2(x))
#         x = F.relu(self.layer_3(x))
#         value = self.value(x)
#         return value

class ActorCritic(nn.Module):
    """
    A unified Actor-Critic network that shares a base feature extractor.
    """

    def __init__(self, embedded_state_dim, total_bt_actions, total_cb_actions):
        super().__init__()

        # Shared base network
        self.base_network = nn.Sequential(
            nn.Linear(embedded_state_dim, 256),
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
        if stage == 'BT':
            action_logits = self.actor_bt_head(base_output)
        elif stage == 'CB':
            action_logits = self.actor_cb_head(base_output)
        else:
            raise ValueError(f"Unknown stage: {stage}")

        return action_logits, state_value.squeeze(-1)  # Squeeze to remove trailing dim

    def sample_action(self, embedded_state, action_mask, stage):

        # Compute action logits
        action_logits, value = self.forward(embedded_state, stage)

        # Apply the action mask
        # We set the logits of illegal actions to a very large negative number.
        # This makes their probability effectively zero after the softmax.
        masked_logits = action_logits.clone()  # Use clone to avoid in-place modification issues
        masked_logits[~action_mask] = -1e9

        # Create categorical distribution
        dist = torch.distributions.Categorical(logits=action_logits)

        # Sample action
        action = dist.sample()

        # Compute log probability of the sampled action
        log_prob = dist.log_prob(action).unsqueeze(-1)

        return action, log_prob


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
        self.network = nn.Sequential(
            nn.Linear(feature_vector_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, embedding_dim)  # The final layer outputs the embedding.
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

    def __init__(self, num_actions, card_feature_length, embedding_dim=512, learning_enabled=True,
                 lr=0.0005, gamma=0.99, epsilon=0.2, entropy_coef=0.02, entropy_decay=0.99, learn_epochs=8):
        # Hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon
        self.entropy_coef = entropy_coef
        self.entropy_decay = entropy_decay
        self.learn_epochs = learn_epochs
        self.learning_enabled = learning_enabled

        # Device configuration
        # self.device = torch.device(
        #     "mps" if torch.backends.mps.is_available() else
        #     "cuda" if torch.cuda.is_available() else "cpu"
        # )
        self.device = torch.device("cpu")
        print(f"Using device: {self.device}")

        # Card Embeddings
        self.card_embed_dim = 512
        self.card_embedding = CardEncoder(card_feature_length, embedding_dim)

        self.max_cards, self.max_enemies = num_actions[0]
        self.max_card_choices = num_actions[1]

        # Initialize actors and critics for each agent
        self.state_dim = 512 + 12
        self.actor_critic = ActorCritic(self.state_dim, self.max_cards * self.max_enemies, self.max_card_choices).to(self.device)

        self.old_network = ActorCritic(self.state_dim, num_actions[0], num_actions[1]).to(self.device)

        self.old_network.load_state_dict(self.actor_critic.state_dict())

        # Optimizers
        params = list(self.actor_critic.parameters()) + list(self.card_embedding.parameters())
        self.optimizer = optim.Adam(params, lr=lr)

        # Memory parameters
        self.memory = {
            'states': [],
            'actions': [],
            'rewards': [],
            'dones': [],
            'log_probs': []
        }
        self.batch_size = 128
        self.learn_size = 8000
        self.max_memory = 1_000_000

        self.learn_step_counter = 0

    def remember(self, states, actions, rewards, dones, log_probs):
        """Store experience for multiple agents"""
        self.memory['states'].append(states)
        self.memory['actions'].append(actions)
        self.memory['rewards'].append(rewards)
        self.memory['dones'].append(dones)
        self.memory['log_probs'].append(log_probs)

        # Trim memory if exceeds max size
        if len(self.memory['states']) > self.max_memory:
            for key in self.memory:
                self.memory[key].pop(0)

    def embed_state(self, state):
        """
        Embeds the raw state dictionary into a single flat tensor for the actor/critic.

        Args:
            state (dict): A dictionary with 'deck' and 'features'.
                          - state['deck']: A tensor of card feature vectors.
                                           Shape: (num_cards_in_deck, card_feature_vector_dim)
                          - state['features']: A flat tensor of other game state features.

        Returns:
            torch.Tensor: A single, flat feature vector representing the combined state.
        """
        # Note: The input 'deck' should be the tensor of raw feature vectors, not embeddings yet.

        # Grab features which are guaranteed to be in the state dictionary.
        deck_card_features = state['deck'].to(self.device)
        player = state['player'].to(self.device)

        # Handle the edge case where the deck is empty (e.g., at the very start of a run).
        if deck_card_features.shape[0] == 0:
            # If there are no cards, the deck's representation is just a zero vector.
            deck_embed = torch.zeros(self.card_embed_dim, device=self.device)
        else:
            # 1. Get embeddings for all cards in the deck.
            #    The CardEncoder handles the transformation from features to embeddings.
            #    Input shape: (num_cards_in_deck, feature_dim)
            #    Output shape: (num_cards_in_deck, card_embed_dim)
            deck_card_embeddings = self.card_embedding(deck_card_features)

            # 2. Aggregate the embeddings into a single vector using mean.
            #    We average across dimension 0 (the list of cards).
            #    This will always result in a tensor of shape (card_embed_dim,).
            deck_embed = torch.mean(deck_card_embeddings, dim=0)

        # Now we will deal with features which may or may not be in the state dict depending on game stage.
        if 'card_choices' in state.keys():
            stage = self.GameStage.CARD_BUILD
            choices_embed = state['card_choices'].to(self.device)
            choices_embed = self.card_embedding(choices_embed)
            choices_embed = torch.flatten(choices_embed)

            hand_embed = torch.zeros((self.max_cards, self.card_embed_dim), device=self.device)
            enemies_embed = torch.zeros((self.max_enemies * 13))
        else:
            stage = self.GameStage.BATTLE
            choices_embed = torch.zeros((self.max_card_choices, self.card_embed_dim), device=self.device)

            hand_embed = self.card_embedding(state['hand'])
            enemies_embed = state['enemies']

            hand_embed = torch.flatten(hand_embed)
            enemies_embed = torch.flatten(enemies_embed)


        # 3. Concatenate the single deck embedding vector with the other state features.
        return torch.cat((deck_embed, player, hand_embed, enemies_embed, choices_embed)), state['action_mask'], stage

    def choose_action(self, state, stage, action_mask):
        """Choose actions for agent"""
        if isinstance(state, dict):
            state = self._convert_state_to_tensors(state)
            state = self.embed_state(state)

        if stage == self.GameStage.CARD_BUILD:
            pass
        else:
            pass

        self.actor_critic.eval()
        with torch.no_grad():
            agent_action, agent_log_prob = self.actor_critic.sample_action(state, stage)

        self.actor_critic.train()

        return agent_action, agent_log_prob

    # def _compute_gae(self, rewards, values, dones, lambda_=0.95):
    #     """Compute Generalized Advantage Estimation"""
    #     advantages = []
    #     gae = 0
    #
    #     # add terminating value
    #     values = np.append(values, 0)
    #
    #     # Reverse iteration
    #     for t in reversed(range(len(rewards))):
    #         delta = rewards[t] + self.gamma * values[t + 1] * (1 - dones[t]) - values[t]
    #         gae = delta + self.gamma * lambda_ * (1 - dones[t]) * gae
    #         advantages.insert(0, gae)
    #
    #     return advantages

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
        states_all = torch.tensor(
            np.array(self.memory['states']),
            dtype=torch.float32
        ).to(self.device)
        actions_all = torch.tensor(
            np.array(self.memory['actions']),
            dtype=torch.float32
        ).to(self.device)
        rewards_all = torch.tensor(
            np.array(self.memory['rewards']),
            dtype=torch.float32
        ).to(self.device)
        dones_all = torch.tensor(
            np.array(self.memory['dones']),
            dtype=torch.float32
        ).to(self.device)

        # values = self.update_critic()
        for i in range(self.learn_epochs):
            num_batches = self.learn_size // self.batch_size
            for batch in range(1, num_batches):
                start_batch = (batch-1) * self.batch_size
                end_batch = batch * self.batch_size

                states = states_all[start_batch:end_batch]
                actions = actions_all[start_batch:end_batch]
                rewards = rewards_all[start_batch:end_batch]
                dones = dones_all[start_batch:end_batch]

                """Update network weights using PPO"""

                # print(actions.shape)

                # Compute advantages using GAE
                # advantages = torch.tensor(x
                #     self._compute_gae(rewards, values.detach().cpu().numpy(),
                #                       dones.detach().cpu().numpy()),
                #     dtype=torch.float32
                # ).to(self.device)
                advantages = torch.tensor(
                    self._compute_vanilla_pg_advantage(rewards, values.detach().cpu().numpy(),
                                      dones.detach().cpu().numpy()),
                    dtype=torch.float32
                ).to(self.device)
                # print(advantages)

                # Normalize advantages
                # advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
                old_log_prob, old_entropy = self._compute_log_prob(self.old_network, states, actions)
                # Recompute log probabilities
                new_log_prob, new_entropy = self._compute_log_prob(self.actor_critic, states, actions)

                # Compute PPO loss
                ratios = torch.exp(new_log_prob - old_log_prob)
                surr1 = ratios * advantages
                surr2 = torch.clamp(ratios, 1 - self.epsilon, 1 + self.epsilon) * advantages
                policy_loss = -torch.min(surr1, surr2).mean()

                # Entropy loss
                entropy_loss = -new_entropy.mean()

                # Total loss
                actor_loss = (policy_loss +
                              self.entropy_coef * entropy_loss)

                # Update actor
                self.optimizer.zero_grad()

                actor_loss.backward()

                # Gradient clipping
                # if self.learn_step_counter > 1000:
                #     torch.nn.utils.clip_grad_norm_(self.actors[agent_idx].parameters(), max_norm=0.5)

                self.optimizer.step()

        self.old_network.load_state_dict(self.actor_critic.state_dict())

        self.entropy_coef *= self.entropy_decay

        # Clear memory after learning
        for key in self.memory:
            self.memory[key].clear()

        self.learn_step_counter += 1

    def update_critic(self):
        # Compute values for all agents
        all_states = torch.tensor(
            np.array(self.memory['states']),
            dtype=torch.float32
        ).to(self.device)
        rewards = torch.tensor(
            np.array(self.memory['rewards']),
            dtype=torch.float32
        ).to(self.device)
        dones = torch.tensor(
            np.array(self.memory['dones']),
            dtype=torch.float32
        ).to(self.device)

        critic_values = self.actor_critic(all_states).squeeze()
        critic_next_values = torch.cat([critic_values[1:], torch.zeros(1).to(self.device)])
        critic_next_values = critic_next_values

        mean_rewards = rewards.mean(dim=1)

        # print("States shape:", all_agent_states.shape)
        # print("Actions shape:", all_agent_actions.shape)
        # print("Rewards shape:", mean_rewards.shape)
        # print("Dones shape:", dones.shape)
        # print("Critic values shape:", critic_values.shape)

        td_target = mean_rewards + self.gamma * critic_next_values * (1 - dones)
        critic_loss = F.mse_loss(critic_values, td_target.detach())
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        # torch.nn.utils.clip_grad_norm_(self.critic.parameters(), max_norm=0.5)
        self.critic_optimizer.step()

        return critic_values

    def _compute_log_prob(self, actor, states, actions):
        """Compute log probabilities and entropy for an agent"""
        logits = actor.forward(states)
        dist = torch.distributions.Categorical(logits=logits)

        # Compute log probabilities
        new_log_probs = dist.log_prob(actions)

        # Compute entropy
        entropy = dist.entropy().sum(dim=-1)

        return new_log_probs, entropy

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
        # Ensure the 'features' array is at least 1D, which torch.from_numpy expects
        features_np = np.atleast_1d(state_np['deck'])
        tensors = {}
        for key, value in state_np.items():
            tensors[key] = torch.from_numpy(value).float().to(self.device)
        return tensors

    def step(self, prev_state, action_taken, log_prob, reward, done, new_state):
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

        embedded_prev_state, action_mask = self.embed_state(prev_state_tensor)
        embedded_new_state, action_mask = self.embed_state(new_state_tensor)
        # Store experiences
        if self.learning_enabled:
            self.remember(embedded_prev_state, action_taken, reward, done, log_prob)

        # Sample actions
        action, log_prob = self.choose_action(embedded_new_state)

        # Learn if enough experiences are collected
        if self.learning_enabled and len(self.memory['states']) >= self.learn_size:
            self._learn()

        return action, log_prob

    def save_models(self, filepath):
        """Save all model weights"""
        checkpoint = {
            'actor_critic': self.actor_critic.state_dict(),
            'optimizer': self.optimizer.state_dict(),
        }
        torch.save(checkpoint, filepath)

    def load_models(self, filepath):
        """Load all model weights"""
        checkpoint = torch.load(filepath)

        self.actor_critic.load_state_dict(checkpoint['actor'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
