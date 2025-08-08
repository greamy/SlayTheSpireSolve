import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


class Actor(nn.Module):
    def __init__(self, num_inputs, num_actions, num_neurons=128):
        super(Actor, self).__init__()

        self.layer_1 = nn.Linear(num_inputs, 256)
        self.layer_2 = nn.Linear(256, 128)
        self.layer_3 = nn.Linear(128, 64)
        self.action_head = nn.Linear(64, num_actions)


    def forward(self, state):
        x = F.relu(self.layer_1(state))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))

        # Compute action logits
        action_logits = self.action_head(x)

        return action_logits

    def sample_action(self, state):
        # Compute action logits
        action_logits = self.forward(state)

        # Create categorical distribution
        dist = torch.distributions.Categorical(logits=action_logits)

        # Sample action
        action = dist.sample()

        # Compute log probability of the sampled action
        log_prob = dist.log_prob(action).unsqueeze(-1)

        return action, log_prob, action_logits


class Critic(nn.Module):
    def __init__(self, state_dim, num_neurons=128):
        super(Critic, self).__init__()

        # Total input will be: (96 observations)
        total_input_dim = state_dim

        self.layer_1 = nn.Linear(total_input_dim, 256)
        self.layer_2 = nn.Linear(256, 128)
        self.layer_3 = nn.Linear(128, 64)
        self.value = nn.Linear(64, 1)

    def forward(self, states):
        x = states[:, 0]

        # Concatenate all observations and actions
        # x = torch.cat([states], dim=-1)

        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        value = self.value(x)
        return value

class PPOAgent:
    def __init__(self, num_inputs, num_actions, card_vocab_size, learning_enabled=True,
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
        self.card_embedding = nn.Embedding(card_vocab_size, 512)


        # Initialize actors and critics for each agent
        self.actor = Actor(num_inputs, num_actions).to(self.device)

        self.old_actor = Actor(self.actor.layer_1.in_features, self.actor.action_head.out_features).to(self.device)

        self.old_actor.load_state_dict(self.actor.state_dict())

        self.critic = Critic(num_inputs).to(self.device)

        # Optimizers
        self.actor_optimizer = optim.Adam(self.actor.parameters() + self.card_embedding.parameters(), lr=lr)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr)

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
        deck = state[0]
        the_rest = state[1]

        deck_embed = self.card_embedding(deck) # nx512, n=number of cards in the deck
        deck_embed = F.avg_pool2d(deck_embed, kernel_size=2, stride=2) # length 512 vector?
        return torch.cat((deck_embed, the_rest)).to(self.device) # 512 + rest of state

    def choose_actions(self, state):
        """Choose actions for all agents"""
        state = torch.tensor(state, dtype=torch.float32).to(self.device)

        self.actor.eval()
        with torch.no_grad():
            agent_action, agent_log_prob, agent_logits = self.actor.sample_action(state)


        self.actor.train()

        return agent_action, agent_log_prob, agent_logits

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

        values = self.update_critic()
        for i in range(self.learn_epochs):
            num_batches = self.learn_size // self.batch_size
            for batch in range(1, num_batches):
                start_batch = (batch-1) * self.batch_size
                end_batch = batch * self.batch_size

                states = states_all[start_batch:end_batch]
                actions = actions_all[start_batch:end_batch]
                rewards = rewards_all[start_batch:end_batch]
                dones = dones_all[start_batch:end_batch]

                """Update network weights using Multi-Agent PPO"""

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
                old_log_prob, old_entropy = self._compute_log_prob(self.old_actor, states, actions)
                # Recompute log probabilities
                new_log_prob, new_entropy = self._compute_log_prob(self.actor, states, actions)

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
                self.actor_optimizer.zero_grad()

                actor_loss.backward()

                # Gradient clipping
                # if self.learn_step_counter > 1000:
                #     torch.nn.utils.clip_grad_norm_(self.actors[agent_idx].parameters(), max_norm=0.5)

                self.actor_optimizer.step()

        self.old_actor.load_state_dict(self.actor.state_dict())

        self.entropy_coef *= self.entropy_decay

        # Clear memory after learning
        for key in self.memory:
            self.memory[key].clear()

        self.learn_step_counter += 1

    def update_critic(self):
        # Compute values for all agents
        all_agent_states = torch.tensor(
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

        critic_values = self.critic(all_agent_states).squeeze()
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

    def step(self, prev_state, action_taken, log_probs, rewards, dones, new_state):
        """
        Take a step for all agents and potentially learn

        Args:
            states: Current states for all agents
            rewards: Rewards for all agents
            next_states: Next states for all agents
            dones: Done flags for all agents

        Returns:
            actions: Chosen actions for all agents
        """
        new_state = self.embed_state(new_state)
        # Store experiences
        if self.learning_enabled:
            self.remember(prev_state, action_taken, rewards, dones, log_probs)

        # Sample actions
        actions, log_probs, logits = self.choose_actions(new_state)


        # Learn if enough experiences are collected
        if self.learning_enabled and len(self.memory['states']) >= self.learn_size:
            self._learn()

        return actions, log_probs, logits

    def save_models(self, filepath):
        """Save all model weights"""
        checkpoint = {
            'actors': self.actor.state_dict(),
            'critic': self.critic.state_dict(),
            'actor_optimizers': self.actor_optimizer.state_dict(),
            'critic_optimizer': self.critic_optimizer.state_dict()
        }
        torch.save(checkpoint, filepath)

    def load_models(self, filepath):
        """Load all model weights"""
        checkpoint = torch.load(filepath)

        for i in range(self.num_agents):
            self.actors[i].load_state_dict(checkpoint['actors'][i])
            self.critic.load_state_dict(checkpoint['critic'])
            self.actor_optimizers[i].load_state_dict(checkpoint['actor_optimizers'][i])
            self.critic_optimizer.load_state_dict(checkpoint['critic_optimizer'])
