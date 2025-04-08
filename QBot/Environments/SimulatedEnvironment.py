import copy
import importlib
import os
import random

import numpy as np

from Combat import Combat
from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.Eruption import Eruption
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Actions.Library.Vigilance import Vigilance
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player

# TODO: Convert class to environment to train a model. Take tensorflow model as input, contains 'train' and 'test' routines
#           which can run the bot in the simulator.
class SimulatedEnvironment():
    def __init__(self, model, target_model, debug: bool=True, act=1, ascension=20, path_to_sim=os.path.join(os.path.curdir, "CombatSim")):
        super().__init__()
        self.model = model
        self.target_model = target_model
        self.debug = debug
        self.act= 1
        self.ascension = 20
        self.path_to_sim = path_to_sim

    def create_player(self):
        return Player(100, 3, 50, [], [], [])

    def create_enemies(self):
        # TODO: Talk to Lucas about possibly having pre-made combats or at least more consistent than random
        num_enemies = random.randint(1, 3)
        possible_enemies = np.array(os.listdir(os.path.join(self.path_to_sim, "Entities\\Dungeon")))[:-1]
        enemy_files = np.random.choice(possible_enemies, num_enemies)
        enemies = np.array([])
        print(enemy_files)
        for enemy in enemy_files:
            if ".py" not in enemy:
                continue
            enemy = enemy[:-3]  # get rid of '.py'
            module = importlib.import_module("CombatSim.Entities.Dungeon." + enemy)
            class_ = getattr(module, enemy)
            enemies = np.append(enemies, class_(self.act, self.ascension))
        return list(enemies)

    def create_deck(self, player: Player):
        # TODO: Talk to  lucas about how to generate a realistic deck
        num_cards = random.randint(7, 20)
        possible_cards = np.array(os.listdir(os.path.join(self.path_to_sim, "Actions/Library/")))[:-1]
        card_files = np.random.choice(possible_cards, num_cards)
        cards = np.array([])
        for card in card_files:
            if ".py" not in card:
                continue
            card = card[:-3]
            module = importlib.import_module("CombatSim.Actions.Library." + card)
            class_ = getattr(module, card)
            try:
                cards = np.append(cards, class_(player))
            except TypeError:
                continue
        return list(cards)

    def create_starter_deck(self, player: Player):
        cards = [Strike(player) for i in range(4)]
        cards.extend([Defend(player) for i in range(4)])
        cards.append(Vigilance(player))
        cards.append(Eruption(player))
        return cards

    def train_model(self, epochs=20, gamma=0.9, rar=0.2, radr=0.99):
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
        played_cards = []
        card_efficiency = []
        for epoch in range(epochs):
            enemies = self.create_enemies()
            self.player = self.create_player()
            cards = self.create_deck(self.player)
            # cards = self.create_starter_deck(self.player)
            self.player.deck = Player.Deck(cards)
            self.combat = Combat(self.player, enemies, self.debug)

            self.player.begin_combat(enemies, self.debug)
            self.player.start_turn(enemies, self.debug)
            deck_state, state = self.combat.get_state()
            last_state = state

            step = 0
            enemy_start_health = self.combat.get_total_enemy_health()
            while self.combat.get_total_enemy_health() > 0 and self.player.is_alive():
                # TODO: Make use of target network to get target values and call model.train() with these target values.
                # deep q network - updated every step
                # target network - only updated every ~10 steps
                #   weights are copied from the deep q network to the target network every ~10 steps
                deck_state = deck_state.reshape(1, -1)
                state = state.reshape(1, -1)
                if self.debug:
                    q_vals = self.model.predict([deck_state, state], verbose=1)[0]
                else:
                    q_vals = self.model.predict([deck_state, state], verbose=0)[0]

                playable_mask = np.array([card.playable and card.energy <= self.player.energy for card in self.player.deck.hand])

                # Pad the playable_mask to match the length of q_vals with True values
                playable_mask = np.pad(playable_mask, (0, len(q_vals) - len(playable_mask)), constant_values=False)

                # Set Q-values for unplayable cards to low_value
                masked_qs = copy.deepcopy(q_vals)
                masked_qs[~playable_mask] = -1_000

                if self.debug:
                    print(masked_qs)

                if random.random() < rar:
                    if self.debug:
                        print("Choosing random...")
                    action = random.randint(0, len(self.player.deck.hand)-1)
                else:
                    if self.debug:
                        print("Choosing best...")
                    action = np.argmax(masked_qs)

                if self.debug:
                    print("action: ", action)

                card = self.player.deck.hand[action]
                played_cards.append(card.name)

                if self.debug:
                    print('[', end='')
                    for c in self.player.deck.hand:
                        print(c, end=', ')
                    print(']')

                new_state, reward = self.combat.run_turn(card, enemies[0])

                if new_state is None:  # player or all enemies died
                    target_q = reward
                else:
                    new_deck_state, new_state = new_state
                    new_deck_state = new_deck_state.reshape(1, -1)
                    new_state = new_state.reshape(1, -1)
                    if self.debug:
                        future_qs = self.target_model.predict([new_deck_state, new_state], verbose=1)
                    else:
                        future_qs = self.target_model.predict([new_deck_state, new_state], verbose=0)
                    max_future_q = np.max(future_qs)

                    target_q = reward + gamma * max_future_q

                target_qs = q_vals
                target_qs[action] = target_q
                target_qs = target_qs.reshape(1, -1)

                # TODO: use target network to predict future q values given that action
                # target = reward + gamma * max(self.target_model.predict([new_deck_state, new_state]))
                # loss = (target - q)**2
                if self.debug:
                    self.model.fit([deck_state, state], target_qs, verbose=1)
                else:
                    self.model.fit([deck_state, state], target_qs, verbose=0)
                if new_state is not None:
                    deck_state, state = new_deck_state, new_state

                if step % 10 == 0:
                    self.target_model.set_weights(self.model.get_weights())

                step += 1

            card_efficiency.append(step/enemy_start_health)
            if epoch % 10 == 0:
                print("********* Epoch " + str(epoch) + " completed!***********")

        return played_cards, card_efficiency
