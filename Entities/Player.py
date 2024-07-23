from Entities.Entity import Entity
import random
from enum import Enum
from Actions.Listener import Listener


class Player(Entity):
    def __init__(self, health: int, status_list: list, energy: int,
                 gold: int, potions: list, relics: list, cards: list):
        super().__init__(health, status_list)
        self.energy = energy
        self.gold = gold
        self.potions = potions
        self.relics = relics
        self.deck = self.Deck(cards)
        self.draw_amount = 5
        self.max_energy = 3
        self.mantra = 0
        self.stance = self.Stance.NONE
        self.listeners = []

    def begin_combat(self):
        # TODO: Ensure all cards are in the draw pile, not in discard or exhaust
        self.deck.begin_combat()
        self.deck.shuffle()

    def end_combat(self):
        self.mantra = 0

    def start_turn(self, enemies, debug):
        super().start_turn(enemies, debug)
        self.energy = self.max_energy
        self.draw_cards(self.draw_amount)
        self.notify_listeners(Listener.Event.START_TURN, enemies, debug)

    def do_turn(self, enemies, debug):
        # TODO: Make player play potions
        while self.energy > 0 and len(self.deck.hand) > 0:
            card_choice = random.choice(self.deck.hand)
            targeted_enemy = random.choice(enemies)
            success = self.play_card(card_choice, targeted_enemy, enemies, debug)
            if not success:
                for card in self.deck.hand:
                    if card.energy <= self.energy:
                        success = self.play_card(card, targeted_enemy, enemies, debug)
                        break

            if not success:
                break
            else:
                for enemy in enemies:
                    if not enemy.is_alive():
                        enemies.remove(enemy)
                if len(enemies) == 0:
                    return

        self.deck.end_turn(debug)
        if self.stance == self.Stance.DIVINITY:
            self.set_stance(self.Stance.NONE)

        self.notify_listeners(Listener.Event.END_TURN, enemies, debug)

    def draw_cards(self, amount):
        self.deck.draw_cards(amount)

    def play_card(self, card, enemy, enemies, debug):
        if card not in self.deck.hand:
            if debug:
                print("Played card does not exist in hand")
            return False
        if card.energy > self.energy:
            if debug:
                print(card.name + " costs too much energy!")
            return False
        self.energy -= card.energy
        card.play(self, enemy, enemies, debug)
        if not card.exhaust:
            self.deck.discard(self.deck.hand.index(card))
        return True

    def gain_block(self, amount):
        self.block += amount

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
        pre_remainder = self.mantra // 10
        self.mantra += amount
        if pre_remainder < self.mantra // 10:
            self.set_stance(self.Stance.DIVINITY)

    def get_mantra_count(self):
        return self.mantra % 10

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, event_type, enemies, debug):
        if debug:
            print("Triggering listeners!")
        for listener in self.listeners:
            if listener.event_type == event_type:
                # TODO: Don't always randomly choose enemy for power target
                listener.notify(self, random.choice(enemies), enemies, debug)

    def __str__(self):
        return "PLAYER\nHealth: " + str(self.health) + "\nBlock: " + str(self.block) + "\nDeck: " + str(self.deck)

    class Stance(Enum):
        NONE = 0
        WRATH = 1
        CALM = 2
        DIVINITY = 3

    class Deck:
        MAX_HAND_SIZE = 10

        def __init__(self, cards):
            self.draw_pile = cards
            self.hand = []
            self.discard_pile = []
            self.exhaust_pile = []

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
            self.shuffle()

        def draw(self, amount):
            self.hand.extend([self.draw_pile.pop(0) for i in range(amount)])

        def discard(self, index):
            self.discard_pile.append(self.hand.pop(index))

        def exhaust(self, card):
            self.exhaust_pile.append(card)
            self.hand.remove(card)

        def begin_combat(self):
            self.reshuffle()
            self.draw_pile.extend(self.hand)
            self.hand.clear()
            self.draw_pile.extend(self.exhaust_pile)
            self.exhaust_pile.clear()
            self.shuffle()

        def end_turn(self, debug):
            temp_hand = [card for card in self.hand if not card.retain]
            self.discard_pile.extend(temp_hand)
            self.hand = [card for card in self.hand if card not in temp_hand]
            if debug:
                print("**************** TURN OVER ****************")

        def __str__(self):
            return ("Draw Pile:" + str([str(card) for card in self.draw_pile]) +
                    "\nHand: " + str([str(card) for card in self.hand]) +
                    "\nDiscard: " + str([str(card) for card in self.discard_pile]) +
                    "\nExhaust: " + str([str(card) for card in self.exhaust_pile]))
