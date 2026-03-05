import copy
import random
from collections import deque

import numpy as np

from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from GameSim.Input.Controller import PlayerController
from GameSim.Input.LSTM_PPO import LSTMPPOAgent
from GameSim.Map.Map import Map
from GameSim.Map.Room import Room


class RLPlayerController(PlayerController):

    def __init__(self, filepath, delay=0, train=True, save=True, visualizer=None):
        super().__init__()
        self.visualizer = visualizer
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
        self.player_vector_length = 11
        self.enemy_vector_length = 12
        self.strategic_vector_length = 10

        self.card_cache = []
        self.path = None

        self.train = train
        self.save = save

        self.prev_obs = None
        self.action_choice = None
        self.log_prob = None
        self.value = None
        self.reward = 0

        self.turn_stable_hand = []
        self.final_healths = []
        self.turn_counts = []
        self.cards_played_counts = []
        self.combats_per_episode = []
        self.wins_per_episode = []
        self.combats_this_episode = 0
        self.reward_history = deque(maxlen=100)

        self.health = 0
        self.start_health = 70
        self.enemy_health = 0
        self.combat_start_health = 0
        self.episode_count = 0

        # Current combat tracking
        self.current_turn_count = 0
        self.current_cards_played = 0

        self.action_space = {"BT": [self.max_num_cards, self.max_num_enemies, 1], "CB": 3}
        self.num_bt_actions = (self.max_num_cards * self.max_num_enemies) + 1

        # self.agent = PPOAgent(self.action_space, self.card_vector_length, 13,
                              # learning_enabled=self.train, filepath=filepath)
        self.agent = LSTMPPOAgent(self.action_space, self.card_vector_length,
                                  self.player_vector_length, self.enemy_vector_length, self.strategic_vector_length,
                                  learning_enabled=self.train, filepath=filepath, save_model=self.save,
                                  visualizer=self.visualizer)

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
            player.mantra
        ])

    def get_enemy_vector(self, enemy: Enemy):
        # if enemy is None:
        #     return np.zeros(13)
        return np.array([
            enemy.start_health / enemy.health if enemy.health > 0 else 0.0,
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
        deck_list = [self.get_card_vector(card, player, enemies) for card in deck_cards]
        deck = np.array(deck_list) if deck_list else np.zeros((0, self.card_vector_length), dtype=np.float32)
        hand_list = [self.get_card_vector(card, player, enemies) if in_hand else self.get_card_vector(None, None, None) for card, in_hand in self.turn_stable_hand]
        hand = np.array(hand_list) if hand_list else np.zeros((0, self.card_vector_length), dtype=np.float32)

        num_enemies = len(enemies)
        if num_enemies > 0:
            enemies_arr = np.array([self.get_enemy_vector(enemy) for enemy in enemies])
        else:
            enemies_arr = np.zeros((0, self.enemy_vector_length), dtype=np.float32)
        if num_enemies < self.max_num_enemies:
            pad = np.zeros((self.max_num_enemies - num_enemies, self.enemy_vector_length), dtype=np.float32)
            enemies_arr = np.concatenate([enemies_arr, pad], axis=0)

        enemy_mask = np.array([i >= num_enemies for i in range(self.max_num_enemies)], dtype=bool)

        state_dict = {
            "deck": deck,
            "player": self.get_player_vector(player),
            "strategic": self.get_strategic_features(player, enemies),
            "action_mask": self.get_battle_action_mask(player, enemies, playable),
            "hand": hand,
            "enemies": enemies_arr,
            "enemy_mask": enemy_mask,
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

    def select_cards_from_zone(self, player: Player, zone: Player.Deck.Zone, enemies: list[Enemy], num_cards: int, debug: bool, condition=None, prefer_outlier=False):
        if not self.wait_for_counter():
            return None

        zone_cards = player.deck.get_zone(zone)

        # Keep original zone indices so callers can index directly into the zone list
        eligible = [(orig_idx, card) for orig_idx, card in enumerate(zone_cards)
                    if condition is None or condition(card)]
        if not eligible:
            return None

        eligible_vecs = [self.get_card_vector(card, player, enemies) for _, card in eligible]
        comparison_cards = player.deck.draw_pile + player.deck.hand
        comparison_vecs = [self.get_card_vector(card, player, enemies) for card in comparison_cards]

        selected_local = set()
        while len(selected_local) < min(num_cards, len(eligible)):
            choice = self.agent.choose_card_from_zone(comparison_vecs, eligible_vecs, selected_local, prefer_outlier)
            selected_local.add(choice)

        return [eligible[i][0] for i in selected_local]

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
        self.reward += health_lost * -0.04
        self.reward += damage_done * 0.04
        self.reward_history.append(self.reward)

        self.health = player.health
        self.enemy_health = sum([enemy.health for enemy in enemies])

    def begin_combat(self, player, enemies, debug):
        self.agent.reset_hidden_state()
        self.health = player.health
        self.combat_start_health = player.health
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
            self.combats_per_episode.append(self.combats_this_episode + 1)
            self.wins_per_episode.append(self.combats_this_episode)
            self.combats_this_episode = 0

            # Episode-level terminal rewards
            if player.health > 0:
                health_ratio = player.health / player.start_health
                base_reward = 0.4 + (0.6 * health_ratio) # Episode victory
            else:
                base_reward = -0.6  # Episode failure

            # Include accumulated bonuses (rest sites, max combats, etc.)
            total_reward = self.reward + base_reward

            # Signal episode termination
            self.agent.step(self.prev_obs, self.action_choice, self.log_prob, total_reward, True, state, self.value)

            # Store episode stats
            self.final_healths.append(player.health)
            self.turn_counts.append(self.current_turn_count)
            self.cards_played_counts.append(self.current_cards_played)
        else:
            self.combats_this_episode += 1
            # Mid-episode combat completion
            base_combat_reward = 0.1 + (player.health / player.start_health) * 0.2

            # Include accumulated bonuses (rest sites)
            total_reward = self.reward + base_combat_reward

            # Episode continues (done=False)
            self.agent.step(self.prev_obs, self.action_choice, self.log_prob, total_reward, False, state, self.value)

        if self.visualizer:
            won = player.health > 0
            health_lost = max(self.combat_start_health - player.health, 0)
            self.visualizer.log_combat(
                win=won,
                health_lost=health_lost,
                turns=self.current_turn_count,
                cards_played=self.current_cards_played,
                episode=self.episode_count
            )

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
        self.episode_count += 1
        self.path = None

    def apply_episode_bonus(self, bonus_reward, reason=""):
        """
        Apply bonus reward during episode (e.g., rest site bonus).
        Adds to accumulated reward that will be given at next step.
        """
        self.reward += bonus_reward

        # if reason:
        #     print(f"  Bonus: +{bonus_reward} ({reason})")

    def get_every_path(self, map: Map) -> list[list[Room]]:
        # starter_floors = [room for room in map.map[0] if room is not None] # 5
        final_list = [[room] for room in map.map[0] if room is not None]
        for floor in range(14):
            new_paths = []
            for idx, path in enumerate(final_list):
                avail_rooms_x_values = map.get_avail_floors(floor + 1, path[-1].x)
                if len(avail_rooms_x_values) == 0:
                    raise Exception("YOU FUCKED UP - no available rooms to choose on path")
                elif len(avail_rooms_x_values) == 1:
                    final_list[idx].append(map.map[floor + 1][avail_rooms_x_values[0]])
                    continue
                else:
                    for j, next_x in enumerate(avail_rooms_x_values):
                        if j == len(avail_rooms_x_values)-1: # first split gets joined to current path
                            final_list[idx].append(map.map[floor + 1][next_x])
                            continue
                        new_path = list(path)
                        new_paths.append(new_path)
                        new_paths[-1].append(map.map[floor + 1][next_x])
            final_list.extend(new_paths)
        return final_list

    def get_map_choice(self, player: Player, map: Map, floor: int, room_idx: int):
        if not self.wait_for_counter():
            return None
        if self.path is None:
            all_paths = self.get_every_path(map)
            valid_paths = {i: path for i, path in enumerate(all_paths)}
            # for path in all_paths:
            #     for room_obj in path:
            #         print(room_obj, end=" ")
            #     print()
            room_type_count = [{'M': 0, "S": 0, "?": 0, "R": 0, "E": 0, 'C': 0} for _ in range(len(all_paths))]
            most_num_consecutive = [{'M': 0, "S": 0, "?": 0, "R": 0, "E": 0, 'C': 0} for _ in range(len(all_paths))]
            cur_num_consecutive = [{'M': 0, "S": 0, "?": 0, "R": 0, "E": 0, 'C': 0} for _ in range(len(all_paths))]
            for j, path in enumerate(all_paths):
                last_room_type = ""
                for idx, room in enumerate(path):
                    room_type_count[j][room.type] += 1
                    cur_num_consecutive[j][room.type] += 1
                    if cur_num_consecutive[j][room.type] > most_num_consecutive[j][room.type]:
                        most_num_consecutive[j][room.type] = cur_num_consecutive[j][room.type]
                    if last_room_type != room.type:
                        cur_num_consecutive[j][last_room_type] = 0
                    last_room_type = room.type

            for i in range(len(all_paths)):
                if most_num_consecutive[i]['M'] > 4:
                    valid_paths[i] = None
                if room_type_count[i]['E'] < 1:
                    valid_paths[i] = None
                if room_type_count[i]['S'] > 2:
                    valid_paths[i] = None
                if room_type_count[i]['?'] > 5:
                    valid_paths[i] = None

            paths_to_choose = [path for path in valid_paths.values() if path is not None]
            if len(paths_to_choose) > 0:
                self.path = random.choice(paths_to_choose)
            else:
                self.path = random.choice(all_paths)

        chosen_room = self.path[floor]
        # for room in self.path:
        #     print(room.type, end=" ")
        # print(floor)
        # print(self.path[floor])
        # print(self.path)

        return chosen_room

    def save_agent(self, filepath):
        self.agent.save_models(filepath)
