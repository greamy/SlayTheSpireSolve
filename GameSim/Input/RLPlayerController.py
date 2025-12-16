import random

import numpy as np

from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from GameSim.Input.Controller import PlayerController
from GameSim.Input.LSTM_PPO import LSTMPPOAgent


class RLPlayerController(PlayerController):

    def __init__(self, filepath, delay=0, train=True):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60
        # self.card_probabilities = {}
        # self.end_turn_probability = 0.0
        # self.min_probability = 0.0
        # self.max_probability = 1.0

        self.max_num_enemies = 5
        self.max_num_cards = 10
        self.card_vector_length = 19
        self.player_vector_length = 12
        self.enemy_vector_length = 12
        self.strategic_vector_length = 10

        self.card_cache = []

        self.train = train

        self.prev_obs = None
        self.action_choice = None
        self.log_prob = None
        self.value = None
        self.reward = 0

        self.turn_stable_hand = []
        self.final_healths = []
        self.turn_counts = []
        self.cards_played_counts = []
        self.health = 0
        self.start_health = 70
        self.enemy_health = 0

        # Current combat tracking
        self.current_turn_count = 0
        self.current_cards_played = 0

        self.action_space = {"BT": [self.max_num_cards, self.max_num_enemies, 1], "CB": 3}
        self.num_bt_actions = (self.max_num_cards * self.max_num_enemies) + 1

        # self.agent = PPOAgent(self.action_space, self.card_vector_length, 13,
                              # learning_enabled=self.train, filepath=filepath)
        self.agent = LSTMPPOAgent(self.action_space, self.card_vector_length,
                                  self.player_vector_length + self.strategic_vector_length, self.enemy_vector_length,
                                  learning_enabled=self.train, filepath=filepath)

    def get_enum_value(self, stance):
        stance_val = -1  # Default value for no stance
        if stance is not None:
            stance_val = stance.value
        return stance_val

    def get_card_vector(self, card: Card, player: Player, enemies: list[Enemy]) -> np.array:
        if card is None or player is None or enemies is None:
            # Return a zero vector with the combined length of the manual vector and the text embedding.
            return np.zeros(self.card_vector_length, dtype=np.float32)
        stance_val = self.get_enum_value(card.stance)
        manual_vector = np.array([
            card.energy,
            card.attacks,
            int(stance_val == Player.Stance.CALM),
            int(stance_val == Player.Stance.WRATH),
            int(stance_val == Player.Stance.DIVINITY),
            int(card.upgraded),  # Cast boolean to int (0 or 1)
            card.draw,
            int(card.exhaust),
            int(card.innate),
            int(card.playable)
        ], dtype=np.float32)

        features = []
        incoming_damage = 0
        for enemy in enemies:  # For single enemy
            incoming_damage += enemy.intent.damage * enemy.intent.attacks
        current_block = player.block

        total_card_dmg = (card.damage * card.attacks)
        card_lethal = False
        overkill_amt = False
        for enemy in enemies:
            if (total_card_dmg * player.damage_dealt_multiplier) + player.damage_dealt_modifier >= enemy.health:
                card_lethal = True

            over = total_card_dmg - enemy.health
            if over < overkill_amt:
                overkill_amt = over
        features.extend([
            # Will this card kill an enemy?
            card_lethal,
            # Does this block fully prevent incoming damage?
            float(card.block + current_block >= incoming_damage and current_block < incoming_damage),
            # Damage efficiency (damage per energy)
            (total_card_dmg / max(card.energy, 1)),
            # Block efficiency
            (card.block / max(card.energy, 1)),
            # Overkill amount (negative if not lethal)
            overkill_amt,
            # Block surplus/deficit after this card
            (card.block + current_block - incoming_damage),
        ])
        features.extend([
            float(card.card_type.value == 0),  # Attack
            float(card.card_type.value == 1),  # Skill
            float(card.card_type.value == 2),  # Power
        ])

        # 3. Concatenate them into a single, richer vector
        embedding = np.concatenate((manual_vector, features))
        return embedding

    def get_player_vector(self, player):
        # TODO: Include player status list
        stance_val = player.stance
        return np.array([
            player.energy,
            player.block,
            player.block_modifier,
            player.block_multiplier,
            player.damage_dealt_modifier,
            player.damage_dealt_multiplier,
            player.damage_taken_multiplier,
            int(stance_val == Player.Stance.CALM),
            int(stance_val == Player.Stance.WRATH),
            int(stance_val == Player.Stance.DIVINITY),
            player.energy,
            player.mantra
        ])

    def get_enemy_vector(self, enemy: Enemy):
        # if enemy is None:
        #     return np.zeros(13)
        return np.array([
            enemy.start_health / enemy.health,
            enemy.block,
            enemy.block_modifier,
            enemy.block_multiplier,
            enemy.damage_dealt_modifier,
            enemy.damage_dealt_multiplier,
            enemy.damage_taken_multiplier,
            int(enemy.minion),
            self.get_enum_value(enemy.intent.intent_type),
            enemy.intent.damage,
            enemy.intent.attacks,
            enemy.intent.block
        ])

    def get_battle_action_mask(self, player, enemies, playable):
        """
        Returns a numpy array of True/False values representing the valid actions.
        Args:
           player: Player object in combat
           enemies: List of Enemy objects in combat
           playable: List of card objects in player's hand which are currently playable.
           debug: Debug flag for print statements.
        Returns:
          np.array: Array of True/False values representing the valid actions.
        """
        mask = np.zeros((self.max_num_cards, self.max_num_enemies), dtype=bool)
        playable_set = set(playable)
        num_enemies = len(enemies)

        if num_enemies == 0:
            card_mask = mask.flatten()
            return np.append(card_mask, True)

        for i, (card, is_still_in_hand) in enumerate(self.turn_stable_hand):
            # A slot is playable if the card is still in our hand AND is in the game's current list of playable cards.
            if is_still_in_hand and card in playable_set:
                requires_target = False
                if card.card_type == Card.Type.ATTACK:
                    requires_target = True

                if requires_target:
                    mask[i, :num_enemies] = True
                else:
                    mask[i, 0] = True

        card_mask = mask.flatten()
        full_mask = np.append(card_mask, True)

        return full_mask

    def get_card_build_action_mask(self, card_choices):
        mask = np.zeros(3, dtype=bool)
        mask[:len(card_choices)] = True
        return mask

    def get_strategic_features(self, player, enemies):
        if not enemies:
            return np.zeros(10, dtype=np.float32)

        raw_incoming = 0
        for enemy in enemies:
            raw_incoming += enemy.intent.damage * enemy.intent.attacks if enemy.intent.damage else 0

        playable = [c for c in player.deck.hand if c.playable]
        raw_damage = sum(c.damage * getattr(c, 'attacks', 1) for c in playable)
        raw_block = sum(c.block for c in playable)

        return np.array([
            # === Raw numbers (always accurate, no interpretation) ===
            raw_incoming,
            raw_damage,
            raw_block,
            player.health / player.start_health,
            player.block / raw_incoming if raw_incoming > 0 else 1.0,

            # === Card availability flags (let network learn implications) ===
            float(any(c.stance == Player.Stance.WRATH for c in playable)),  # Has wrath card
            float(any(c.stance == Player.Stance.CALM for c in playable)),  # Has calm card
            float(any(c.block > 0 for c in playable)),  # Has block
            float(any(c.damage > 0 for c in playable)),  # Has damage
            len(playable),
        ], dtype=np.float32)

    def get_battle_state(self, player, enemies, playable, debug) -> dict:
        """
        Get state dict that agent can use from CombatSim objects.

        Args:
            player: Player object in combat
            enemies: List of Enemy objects in combat
            playable: List of card objects in player's hand which are currently playable.
            debug: Debug flag for print statements.

        Returns:
            dict: Dictionary of numpy state vectors to pass to agent.
        """

        deck_cards = player.deck.get_deck()
        deck = np.array([self.get_card_vector(card, player, enemies) for card in deck_cards])
        hand = np.array([self.get_card_vector(card, player, enemies) if in_hand else self.get_card_vector(None, None, None) for card, in_hand in self.turn_stable_hand])

        state_dict = {
            "deck": deck,
            "player": self.get_player_vector(player),
            "strategic": self.get_strategic_features(player, enemies),
            "action_mask": self.get_battle_action_mask(player, enemies, playable),
            "hand": hand,
            "enemies": np.array([self.get_enemy_vector(enemy) for enemy in enemies])
        }
        return state_dict

    def get_choose_card_state(self, player, card_choices, debug):
        deck_cards = player.deck.get_deck()
        deck = np.array([self.get_card_vector(card) for card in deck_cards])
        card_vectors = np.array([self.get_card_vector(c) for c in card_choices])

        state_dict = {
            "deck": deck,
            "player": self.get_player_vector(player),
            "action_mask": self.get_card_build_action_mask(card_choices),
            "card_choices": card_vectors
        }
        return state_dict

    def get_target(self, player, enemies, playable, debug):
        return self.action_choice % self.max_num_enemies, enemies[self.action_choice % self.max_num_enemies]

    def get_scry(self, player, enemies, cards, debug):
        if not self.wait_for_counter():
            return None, None
        to_discard = set()

        for i in range(random.randint(0, len(cards))):
            choice = random.randint(0, len(cards) - 1)
            to_discard.add(choice)
        to_discard = list(to_discard)
        return to_discard

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        if not self.wait_for_counter():
            return None, None
        if len(self.turn_stable_hand) == 0:
            self.start_turn(player, enemies)

        # print(self.reward)
        # self.reward -= 0.01 # small negative each card play to encourage efficient play

        state = self.get_battle_state(player, enemies, playable_cards, debug)
        self.action_choice, self.log_prob, self.value, action_probs = self.agent.step(prev_state=self.prev_obs, action_taken=self.action_choice,
                                                       log_prob=self.log_prob, reward=self.reward, done=False, new_state=state, value=self.value)

        # Calculate per-card probabilities (sum across enemy targets)
        # if action_probs is not None:
        #     self.card_probabilities = {}
        #     for card_idx in range(self.max_num_cards):
        #         start_action = card_idx * self.max_num_enemies
        #         end_action = start_action + self.max_num_enemies
        #         card_prob = action_probs[start_action:end_action].sum()
        #         self.card_probabilities[card_idx] = float(card_prob)
        #
        #     # End turn probability
        #     self.end_turn_probability = float(action_probs[self.num_bt_actions-1])
        #
        #     # Calculate min/max for dynamic color scaling
        #     all_probs = list(self.card_probabilities.values()) + [self.end_turn_probability]
        #     self.min_probability = min(all_probs)
        #     self.max_probability = max(all_probs)

        self.prev_obs = state
        self.reward = 0

        if self.action_choice == self.num_bt_actions-1:
            self.turn_stable_hand = []
            return False, False

        card_index = (self.action_choice // self.max_num_enemies)
        card, is_still_in_hand = self.turn_stable_hand[card_index]
        # print(playable_cards[card_index])

        if is_still_in_hand and card in playable_cards:
            # IMPORTANT: Mark this card as "played" in our stable snapshot
            # so the agent knows it can't be played again this turn.
            self.turn_stable_hand[card_index][1] = False

            # Increment cards played counter
            self.current_cards_played += 1

            # The game engine will handle removing the card from the real player.hand
            return card_index, card
        else:
            raise Exception("Invalid output from PPOAgent. Invalid action: " + card_index + ": " + str(self.turn_stable_hand))

    def select_cards_from_zone(self, player: Player, zone: Player.Deck.Zone, enemies: list[Enemy], num_cards: int, debug: bool):
        if not self.wait_for_counter():
            return None
        selected_indices = set()
        card_choices = player.deck.get_zone(zone)
        card_choices = [self.get_card_vector(card, player, enemies) for card in card_choices]

        comparison_cards = player.deck.draw_pile + player.deck.hand
        comparison_cards = [self.get_card_vector(card, player, enemies) for card in comparison_cards]

        while len(selected_indices) < num_cards:
            choice = self.agent.choose_card_from_zone(comparison_cards, card_choices, selected_indices)
            selected_indices.add(choice)
        return list(selected_indices)

    def start_turn(self, player, enemies):
        """
        Called at the start of a player's turn to create a stable snapshot of the hand.
        """
        # We store a list of tuples: (card_object, is_still_in_hand_bool)
        self.turn_stable_hand = [[card, True] for card in player.deck.hand]

        # Increment turn counter (one turn is a player->enemy cycle)
        self.current_turn_count += 1

        self.reward = 0
        health_lost = self.health - player.health
        damage_done = self.enemy_health - sum([enemy.health for enemy in enemies])
        self.reward += health_lost * -2.0
        self.reward += damage_done * 2.0

        self.health = player.health
        self.enemy_health = sum([enemy.health for enemy in enemies])

    def begin_combat(self, player, enemies, debug):
        self.health = player.health
        self.enemy_health = sum([enemy.health for enemy in enemies])

        # Reset combat-specific counters
        self.current_turn_count = 0
        self.current_cards_played = 0

        self.start_turn(player, enemies)
        playable = player.get_playable_cards()
        state = self.get_battle_state(player, enemies, playable, debug)
        self.action_choice, self.log_prob, self.value, action_probs = self.agent.choose_action(
            self.agent._convert_state_to_tensors(state)
        )

        # Calculate per-card probabilities (sum across enemy targets)
        if action_probs is not None:
            self.card_probabilities = {}
            for card_idx in range(self.max_num_cards):
                start_action = card_idx * self.max_num_enemies
                end_action = start_action + self.max_num_enemies
                card_prob = action_probs[start_action:end_action].sum()
                self.card_probabilities[card_idx] = float(card_prob)

            # End turn probability
            self.end_turn_probability = float(action_probs[self.num_bt_actions-1])

            # Calculate min/max for dynamic color scaling
            all_probs = list(self.card_probabilities.values()) + [self.end_turn_probability]
            self.min_probability = min(all_probs)
            self.max_probability = max(all_probs)

        self.prev_obs = state

    def end_combat(self, player, enemies, debug, episode_done=True):
        """
        Handle end of combat.

        Args:
            episode_done: If True, this is the final combat in episode (terminal state).
                         If False, episode continues (mid-episode combat completion).
        """
        state = self.get_battle_state(player, enemies, player.get_playable_cards(), debug)

        if episode_done:
            # Episode-level terminal rewards
            if player.health > 0:
                health_ratio = player.health / player.start_health
                base_reward = 20 + (30 * health_ratio) # Episode victory
            else:
                base_reward = -30  # Episode failure

            # Include accumulated bonuses (rest sites, max combats, etc.)
            total_reward = self.reward + base_reward

            # Signal episode termination
            self.agent.step(self.prev_obs, self.action_choice, self.log_prob, total_reward, True, state, self.value)

            # Store episode stats
            self.final_healths.append(player.health)
            self.turn_counts.append(self.current_turn_count)
            self.cards_played_counts.append(self.current_cards_played)
        else:
            # Mid-episode combat completion
            base_combat_reward = 5 + (player.health / player.start_health) * 10

            # Include accumulated bonuses (rest sites)
            total_reward = self.reward + base_combat_reward

            # Episode continues (done=False)
            self.agent.step(self.prev_obs, self.action_choice, self.log_prob, total_reward, False, state, self.value)

        # Reset accumulated reward for next combat
        self.reward = 0
        self.prev_obs = state
        self.card_cache = []

    def begin_episode(self):
        """
        Initialize episode-level state.
        Called once at the start of each multi-combat episode.
        """
        self.agent.reset_hidden_state()

    def apply_episode_bonus(self, bonus_reward, reason=""):
        """
        Apply bonus reward during episode (e.g., rest site bonus).
        Adds to accumulated reward that will be given at next step.
        """
        self.reward += bonus_reward

        # if reason:
        #     print(f"  Bonus: +{bonus_reward} ({reason})")

    def get_map_choice(self, player, map_gen, floor, room_idx):
        if not self.wait_for_counter():
            return None
        avail_rooms = map_gen.get_avail_floors(floor, room_idx)
        return map_gen.map[floor][random.choice(avail_rooms)]
