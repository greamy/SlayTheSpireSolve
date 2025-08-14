import random

import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Enemy import Enemy
from GameSim.Input.Controller import PlayerController
from GameSim.Input.PPO import PPOAgent


class RLPlayerController(PlayerController):

    def __init__(self, filepath, delay=0, train=True):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60

        self.max_num_enemies = 5
        self.max_num_cards = 10

        self.card_cache = []

        self.train = train

        self.prev_obs = None
        self.action_choice = None
        self.log_prob = None
        self.value = None

        self.final_healths = []
        self.health = 0
        self.enemy_health = 0

        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.text_model = AutoModel.from_pretrained("distilbert-base-uncased")

        self.agent = PPOAgent([(self.max_num_cards, self.max_num_enemies), 3], 779, 13,
                              learning_enabled=self.train, filepath=filepath)

    def get_enum_value(self, stance):
        stance_val = -1  # Default value for no stance
        if stance is not None:
            stance_val = stance.value
        return stance_val

    def get_card_vector(self, card: Card) -> np.array:
        # if card is None:
        #     return np.zeros(11)

        manual_vector = np.array([ #
            card.card_type.value,
            card.energy,
            card.damage,
            card.attacks,
            card.block,
            self.get_enum_value(card.stance),  # Use the numerical value
            int(card.upgraded),  # Cast boolean to int (0 or 1)
            card.draw,
            int(card.exhaust),
            int(card.innate),
            int(card.playable)
        ], dtype=np.float32)

        if card not in self.card_cache:
            inputs = self.tokenizer(card.description, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.text_model(**inputs)
            # Use the [CLS] token's embedding (the first token)
            text_embedding = outputs.last_hidden_state[0, 0, :].cpu().numpy()

            card.set_text_embedding(text_embedding)
            self.card_cache.append(card)

        # 3. Concatenate them into a single, richer vector
        embedding = np.concatenate((manual_vector, card.text_embedding))
        return embedding

    def get_player_vector(self, player):
        # TODO: Include player status list
        return np.array([
            player.start_health,
            player.health,
            player.block,
            player.block_modifier,
            player.block_multiplier,
            player.damage_dealt_modifier,
            player.damage_dealt_multiplier,
            player.damage_taken_multiplier,
            self.get_enum_value(player.stance),
            player.energy,
            player.mantra
        ])

    def get_enemy_vector(self, enemy: Enemy):
        # if enemy is None:
        #     return np.zeros(13)
        return np.array([
            enemy.start_health,
            enemy.health,
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
        num_playable_cards = len(playable)
        num_enemies = len(enemies)
        if num_playable_cards > 0 and num_enemies > 0:
            mask[:num_playable_cards, :num_enemies] = True

        # 3. Flatten the 2D mask into a 1D vector of size 50.
        return mask.flatten()

    def get_card_build_action_mask(self, card_choices):
        mask = np.zeros(3, dtype=bool)
        mask[:len(card_choices)] = True
        return mask

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
        deck = np.array([self.get_card_vector(card) for card in deck_cards])
        hand = np.array([self.get_card_vector(card) for card in playable])

        state_dict = {
            "deck": deck,
            "player": self.get_player_vector(player),
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
        health_lost = self.health - player.health
        damage_done = self.enemy_health - sum([enemy.health for enemy in enemies])

        reward = -0.1 # small negative each card play to encourage efficient play
        reward += -0.2 * health_lost # larger negative for taking damage
        reward += 0.1 * damage_done # positive reward for doing damage

        state = self.get_battle_state(player, enemies, playable_cards, debug)
        self.action_choice, self.log_prob, self.value = self.agent.step(prev_state=self.prev_obs, action_taken=self.action_choice,
                                                       log_prob=self.log_prob, reward=reward, done=False, new_state=state, value=self.value)

        self.prev_obs = state

        card_index = (self.action_choice // self.max_num_enemies)
        self.health = player.health
        self.enemy_health = sum([enemy.health for enemy in enemies])
        # print(playable_cards[card_index])
        return card_index, playable_cards[card_index]

    def begin_combat(self, player, enemies, debug):
        playable = player.get_playable_cards()
        state = self.get_battle_state(player, enemies, playable, debug)
        self.action_choice, self.log_prob, self.value = self.agent.choose_action(
            self.agent._convert_state_to_tensors(state)
        )

        self.prev_obs = state

    def end_combat(self, player, enemies, debug):
        state = self.get_battle_state(player, enemies, player.get_playable_cards(), debug)
        if player.health > 0:
            reward = 1
        else:
            reward = -1
        self.agent.step(self.prev_obs, self.action_choice, self.log_prob, reward, True, state, self.value)

        self.prev_obs = state
        self.card_cache = []

    def get_map_choice(self, player, map_gen, floor, room_idx):
        if not self.wait_for_counter():
            return None
        avail_rooms = map_gen.get_avail_floors(floor, room_idx)
        return map_gen.map[floor][random.choice(avail_rooms)]
