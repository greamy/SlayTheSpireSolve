import numpy as np

from CombatSim.Actions.Card import Card
from CombatSim.Entities.Enemy import Enemy
from GameSim.Input.Controller import PlayerController
from GameSim.Input.PPO import PPOAgent


class RLPlayerController(PlayerController):

    def __init__(self, delay=0, train=True):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60

        self.max_num_enemies = 5
        self.max_num_cards = 10

        self.train = train

        self.prev_obs = None
        self.action_choice = None
        self.log_prob = None

        self.agent = PPOAgent([(self.max_num_cards, self.max_num_enemies), 3], 100,
                              512, learning_enabled=self.train)

    def get_card_vector(self, card: Card) -> np.array:
        # if card is None:
        #     return np.zeros(11)
        return np.array([card.card_type, card.energy, card.damage, card.attacks,
                         card.block, card.stance, card.upgraded, card.draw, card.exhaust, card.innate, card.playable])

    def get_player_vector(self, player):
        # TODO: Include player status list
        return np.array([player.start_health, player.health, player.block, player.block_modifier, player.block_multiplier,
                         player.damage_dealt_modifier, player.damage_dealt_multiplier, player.damage_taken_multiplier,
                         player.stance, player.energy, player.mantra])

    def get_enemy_vector(self, enemy: Enemy):
        # if enemy is None:
        #     return np.zeros(13)
        return np.array([enemy.start_health, enemy.health, enemy.block, enemy.block_modifier, enemy.block_multiplier,
                         enemy.damage_dealt_modifier, enemy.damage_dealt_multiplier, enemy.damage_taken_multiplier, enemy.minion,
                         enemy.intent.intent_type, enemy.intent.damage, enemy.intent.attacks, enemy.intent.block])

    def get_combat_action_mask(self, player, enemies, playable, debug):
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
        mask = np.array([np.pad([True for enemy in enemies], (0, self.max_num_enemies - len(enemies)))] for card in playable)
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
            "action_mask": np.array([]),
            "hand": hand,
            "enemies": np.array([self.get_enemy_vector(enemy) for enemy in enemies])
        }
        return state_dict

    def choose_card(self, player, card_choices, debug):
        deck_cards = player.deck.get_deck()
        deck = np.array([self.get_card_vector(card) for card in deck_cards])
        card_vectors = np.array([self.get_card_vector(c) for c in card_choices])

        state_dict = {
            "deck": deck,
            "player": self.get_player_vector(player),
            "card_choices": card_vectors
        }
        return state_dict

    def get_target(self, player, enemies, playable, debug):
        return self.action_choice % self.max_num_enemies

    def get_scry(self, player, enemies, cards, debug):
        pass

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        state = self.get_battle_state(player, enemies, playable_cards, debug)
        self.action_choice, self.log_prob = self.agent.step(prev_state=self.prev_obs, action_taken=self.action_choice,
                                                       log_prob=self.log_prob, reward=0, done=False, new_state=state)

        self.prev_obs = state

        card_index = self.action_choice // self.max_num_enemies
        return card_index, playable_cards[card_index]

    def start_combat(self, player, enemies, debug):
        state = self.get_battle_state(player, enemies, player.get_playable_cards(player.deck.hand), debug)
        self.action_choice, self.log_prob = self.agent.choose_action(state)

        self.prev_obs = state

    def end_combat(self, player, enemies, debug):
        state = self.get_battle_state(player, enemies, player.get_playable_cards(player.deck.hand), debug)
        reward = 0
        if player.health > 0:
            reward = 1
        self.agent.step(self.prev_obs, self.action_choice, self.log_prob, reward, True, state)

        self.prev_obs = state

