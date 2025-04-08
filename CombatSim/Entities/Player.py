import importlib
import os

from CombatSim.Entities.Entity import Entity
import random
from enum import Enum
from CombatSim.Actions.Listener import Listener

import numpy as np

from CombatSim.Items.Relics.Relic import Relic


class Player(Entity):
    def __init__(self, health: int, energy: int, gold: int, potions: list, relics: list, cards: list[str], library_path="C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\CombatSim\\Actions\\Library"):
        super().__init__(health)
        self.max_health = health
        self.energy = energy
        self.gold = gold
        self.potions = potions
        self.relics = relics
        self.draw_amount = 5
        self.max_energy = 3
        self.mantra = 0
        self.stance = self.Stance.NONE
        self.turn_over = False
        self.innate_cards = []
        self.relics = []
        # self.implemented_cards = self.get_implemented_cards(library_path)
        self.deck = self.Deck(self.create_deck(cards))

        # self.bot = QBot()

    @staticmethod
    def get_implemented_cards(library_path: str) -> dict:
        my_cards = {}
        card_name_list = os.listdir(os.path.join(os.curdir, library_path))
        module_path = library_path.replace("../", "").replace("/", ".") + "."
        for card_name in card_name_list:
            if card_name.endswith(".py"):
                card_name = card_name[:-3]
                module = importlib.import_module(module_path + card_name)
                my_cards[card_name] = module
        return my_cards

    def add_relic(self, relic: Relic):
        self.relics.append(relic)
        relic.on_pickup()

    def drop_relic(self, relic: Relic):
        self.relics.remove(relic)
        relic.on_drop()

    def create_deck(self, cards: list[str]) -> list:
        deck = []
        for card in cards:
            if card in self.implemented_cards.keys():
                class_ = getattr(self.implemented_cards[card], card)
                deck.append(class_(self))
            else:
                raise Exception(f"No implemented card named {card}")
        return deck

    def begin_combat(self, enemies, debug):
        self.deck.reshuffle()
        num_innate = 0
        for idx, card in enumerate(self.deck.draw_pile):
            if card.innate:
                self.deck.swap(0 + num_innate, idx)
                num_innate += 1

        self.notify_listeners(Listener.Event.START_COMBAT, enemies, debug)

    def end_combat(self):
        self.mantra = 0

    def start_turn(self, enemies, debug):
        super().start_turn(enemies, debug)
        self.energy = self.max_energy
        self.draw_cards(self.draw_amount, enemies, debug)

    def do_turn(self, enemies, debug):
        # TODO: Make player play potions
        playable_cards = self.get_playable_cards()
        while len(playable_cards) > 0 and not self.turn_over:
            # card_choice, targeted_enemy = self.bot.combat_choose_next_action(playable_cards, enemies)
            card_choice = random.choice(playable_cards)
            targeted_enemy = random.choice(enemies)
            success = self.play_card(card_choice, targeted_enemy, enemies, debug)
            if not success:
                playable_cards.remove(card_choice)
                continue

            for enemy in enemies:
                if not enemy.is_alive():
                    enemies.remove(enemy)
            if len(enemies) == 0:
                return
            playable_cards = self.get_playable_cards()

        self.end_turn(enemies, debug)

    def end_turn(self, enemies, debug):
        super().end_turn(enemies, debug)

        self.deck.end_turn(debug)
        self.notify_listeners(Listener.Event.HAND_CHANGED, enemies, debug)
        if len(self.deck.hand) > 0:
            self.notify_listeners(Listener.Event.CARD_RETAINED, enemies, debug)
        if self.stance == self.Stance.DIVINITY:
            self.set_stance(self.Stance.NONE)

        self.turn_over = False

    def draw_cards(self, amount, enemies, debug):
        self.deck.draw_cards(amount)
        self.notify_listeners(Listener.Event.HAND_CHANGED, enemies, debug)

    def discard(self, card, enemies, debug):
        self.deck.discard(card)
        self.notify_listeners(Listener.Event.HAND_CHANGED, enemies, debug)

    def play_card(self, card, enemy, enemies, debug):
        if card not in self.deck.hand:
            if debug:
                print("Played card does not exist in hand")
            return False
        if card.energy > self.energy:
            if debug:
                print(card.name + " costs too much energy!")
            return False
        if not card.playable:
            if debug:
                print(card.name + " is not playable right now.")
            return False
        self.energy -= card.energy
        self.deck.hand.remove(card)
        card.play(self, [self], enemy, enemies, debug)

        if card.is_attack():
            self.notify_listeners(Listener.Event.ATTACK_PLAYED, enemies, debug)
        elif card.is_skill():
            self.notify_listeners(Listener.Event.SKILL_PLAYED, enemies, debug)
        elif card.is_power():
            self.deck.used_powers.append(card)
            self.notify_listeners(Listener.Event.POWER_PLAYED, enemies, debug)
        if card.exhaust:
            self.deck.exhaust_pile.append(card)
        if card not in self.deck.get_deck():
            self.discard(card, enemies, debug)
        return True

    def get_playable_cards(self):
        return [card for card in self.deck.hand if card.energy <= self.energy and card.playable]

    def use_potion(self, potion):
        pass

    def set_stance(self, stance):
        if self.stance == self.Stance.CALM and stance != self.Stance.CALM:
            self.energy += 2
        if self.stance == self.Stance.WRATH and stance != self.Stance.WRATH:
            self.damage_dealt_multiplier /= 2
            self.damage_taken_multiplier /= 2
        if self.stance == self.Stance.DIVINITY and stance != self.Stance.DIVINITY:
            self.damage_dealt_multiplier /= 3

        if self.stance != self.Stance.WRATH and stance == self.Stance.WRATH:
            self.damage_dealt_multiplier *= 2
            self.damage_taken_multiplier *= 2
        if self.stance != self.Stance.DIVINITY and stance == self.Stance.DIVINITY:
            self.damage_dealt_multiplier *= 3
            self.energy += 3

        self.stance = stance

    def add_mantra(self, amount):
        pre_result = self.mantra // 10
        self.mantra += amount
        if pre_result < self.mantra // 10:
            self.set_stance(self.Stance.DIVINITY)

    def get_mantra_count(self):
        return self.mantra % 10

    def scry(self, amount, enemies, debug):
        # TODO: Make better Scry AI
        index = 0
        cards = self.deck.draw_pile[0:amount]
        # to_scry = self.bot.scry(cards, enemies, None)
        to_scry = [random.choice([True, False]) for _ in cards]
        for i, card in enumerate(cards):
            if to_scry[i]:
                self.discard(self.deck.draw_pile.pop(index), enemies, debug)
            else:
                index += 1
        self.notify_listeners(Listener.Event.SCRY_OCCURRED, enemies, debug)

    def gain_gold(self, amount, enemies, debug):
        self.gold += amount
        # TODO: Add gold gained listener notification

    def __str__(self):
        return "PLAYER\nHealth: " + str(self.health) + "\nBlock: " + str(self.block) + "\nDeck: " + str(self.deck)

    class Stance(Enum):
        NONE = 0
        WRATH = 1
        CALM = 2
        DIVINITY = 3

    class Deck:
        MAX_HAND_SIZE = 10
        MAX_CARDS_ENCODING = 25

        def __init__(self, cards):
            self.draw_pile = cards
            self.hand = []
            self.discard_pile = []
            self.exhaust_pile = []
            self.used_powers = []

        def shuffle(self):
            random.shuffle(self.draw_pile)

        def swap(self, first, second):
            tmp = self.draw_pile[first]
            self.draw_pile[first] = self.draw_pile[second]
            self.draw_pile[second] = tmp

        # Return a list of length num of cards
        def draw_cards(self, num):
            if len(self.hand) + num > self.MAX_HAND_SIZE:
                num -= (len(self.hand) + num) - self.MAX_HAND_SIZE
            if num > (len(self.draw_pile) + len(self.discard_pile)):
                num = len(self.draw_pile) + len(self.discard_pile)
            if num > len(self.draw_pile):
                self.hand.extend(self.draw_pile)
                num -= len(self.draw_pile)
                self.draw_pile.clear()
                self.reshuffle()
            for i in range(num):
                self.hand.append(self.draw_pile.pop(0))

        def reshuffle(self):
            self.draw_pile.extend(self.discard_pile)
            self.discard_pile.clear()
            self.draw_pile.extend(self.hand)
            self.hand.clear()
            self.draw_pile.extend(self.exhaust_pile)
            self.exhaust_pile.clear()
            self.draw_pile.extend(self.used_powers)
            self.used_powers.clear()
            self.shuffle()

        def draw(self, amount):
            self.hand.extend([self.draw_pile.pop(0) for i in range(amount)])

        def discard(self, card):
            if card in self.hand:
                self.hand.remove(card)
            self.discard_pile.append(card)

        def exhaust(self, card):
            self.exhaust_pile.append(card)
            self.hand.remove(card)

        def end_turn(self, debug):
            to_discard = [card for card in self.hand if not card.retain and not card.temp_retain]
            self.discard_pile.extend(to_discard)
            self.hand = [card for card in self.hand if card.retain or card.temp_retain]

            if debug:
                print("**************** TURN OVER ****************")

        def get_deck(self, extra_cards=None):
            if extra_cards is None:
                extra_cards = list()
            return self.hand + self.draw_pile + self.discard_pile + self.exhaust_pile + self.used_powers + extra_cards

        def get_state(self):

            hand_state = np.array([card.id for card in self.hand[:self.MAX_HAND_SIZE]])
            hand_state = np.pad(hand_state, (0, max(0, self.MAX_HAND_SIZE - len(hand_state))), constant_values=-1)

            discard_state = np.array([card.id for card in self.discard_pile[:self.MAX_CARDS_ENCODING]])
            discard_state = np.pad(discard_state, (0, max(0, self.MAX_CARDS_ENCODING - len(discard_state))), constant_values=-1)

            draw_state = np.array([card.id for card in self.draw_pile[:self.MAX_CARDS_ENCODING]])
            draw_state = np.pad(draw_state, (0, max(0, self.MAX_CARDS_ENCODING - len(draw_state))), constant_values=-1)

            exhaust_state = np.array([card.id for card in self.exhaust_pile[:self.MAX_CARDS_ENCODING]])
            exhaust_state = np.pad(exhaust_state, (0, max(0, self.MAX_CARDS_ENCODING - len(exhaust_state))), constant_values=-1)

            powers_state = np.array([card.id for card in self.used_powers[:self.MAX_CARDS_ENCODING]])
            powers_state = np.pad(powers_state, (0, max(0, self.MAX_CARDS_ENCODING - len(powers_state))), constant_values=-1)

            state = np.concatenate((hand_state, discard_state, draw_state, exhaust_state, powers_state))
            return state


        def __str__(self):
            return ("Draw Pile:" + str([str(card) for card in self.draw_pile]) +
                    "\nHand: " + str([str(card) for card in self.hand]) +
                    "\nDiscard: " + str([str(card) for card in self.discard_pile]) +
                    "\nExhaust: " + str([str(card) for card in self.exhaust_pile]))
