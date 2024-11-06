import importlib
import os
import random

import numpy as np

from Combat import Combat
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from SpireBot.Environments.Environment import Environment

# TODO: Convert class to environment to train a model. Take tensorflow model as input, contains run 'train' and 'test' routines
#           which can run the bot in the simulator.
class SimulatedEnvironment():
    def __init__(self, model, debug: bool=True, act=1, ascension=20, path_to_sim="./CombatSim"):
        super().__init__()
        self.model = model
        self.target_model = model
        self.debug = debug
        self.act= 1
        self.ascension = 20
        self.path_to_sim = path_to_sim

    def create_player(self):
        return Player(100, 3, 50, [], [], [])

    def create_enemies(self):
        # TODO: Talk to Lucas about possibly having pre-made combats or at least more consistent than random
        num_enemies = random.randint(1, 3)
        possible_enemies = np.array(os.listdir(os.path.join(self.path_to_sim, "Entities/Dungeon")))
        enemy_files = np.random.choice(possible_enemies, num_enemies)
        enemies = np.array([])
        for enemy in enemy_files:
            enemy = enemy[:-3] # get rid of '.py'
            module = importlib.import_module("CombatSim.Entities.Dungeon." + enemy)
            class_ = getattr(module, enemy)
            np.append(enemies, class_(self.act, self.ascension))
        return list(enemies)

    def create_deck(self, player: Player):
        # TODO: Talk to  lucas about how to generate a realistic deck
        num_cards = random.randint(7, 20)
        possible_cards = np.array(os.listdir(os.path.join(self.path_to_sim, "Actions/Library/")))
        card_files = np.random.choice(possible_cards, num_cards)
        cards = np.array([])
        for card in card_files:
            card = card[:-3]
            module = importlib.import_module("CombatSim.Actions.Library." + card)
            class_ = getattr(module, card)
            np.append(cards, class_(player))
        return list(cards)

    def train_model(self, epochs=20):
        """
        Train the model, something along the lines of:
        1. Create combat object with randomized or manually selected enemies and deck configuration to use for training
        2. Run the combat
            a. get state from combat object (this returns deck_state and the rest of the combat state (health vals, intent, etc)
            b. Pass the deck state into an embedding layer
                ba. (optional) pass the other state values into a dense layer on their own
            c. Concatenate the deck state and other state vector together, pass into the rest of the network
            d. Find the output neuron with highest Q value, and take that corresponding action
                - this will require masking out actions that are invalid at the moment
                (ie. the network says to play card #10 in hand, when you only have 6 cards in hand)
            e. Pass the action into the simulated environment and obtain a reward value from the sim. Use this value
                to obtain a 'target q' value with bellman equation (using secondary 'target' network to predict future q's).
            f. use these 'target q' values as labels to run a train step.
            g. Repeat until combat is complete.
        2. Repeat until a number of epochs have been completed
        :return:
        """

        for epoch in range(epochs):
            enemies = self.create_enemies()
            self.player = self.create_player()
            cards = self.create_deck(self.player)
            self.player.deck = Player.Deck(cards)
            combat = Combat(self.create_player(), enemies, self.debug)

            self.player.begin_combat()
            deck_state, state = combat.get_state()
            print(state)
            while combat.get_total_enemy_health() > 0:
                # TODO: Make use of target network to get target values and call model.train() with these target values.
                q_vals = self.model.predict([deck_state, state])
                action = np.argmax(q_vals)
                # TODO: convert action index to actual card to be played/potion to be used and enemy to play it on.

                # combat.run_turn()

 