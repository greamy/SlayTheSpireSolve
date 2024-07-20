# this is the area where you are going to make cards
import random
from Card import Card


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
        if num > len(self.draw_pile):
            self.hand.extend(self.draw_pile)
            num -= len(self.draw_pile)
            self.reshuffle()
            self.draw_cards(num)
            return
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

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand.clear()
        print("**************** TURN OVER ****************")

    def __str__(self):
        return ("Draw Pile:" + str([str(card) for card in self.draw_pile]) +
                "\nHand: " + str([str(card) for card in self.hand]) +
                "\nDiscard: " + str([str(card) for card in self.discard_pile]) +
                "\nExhaust: " + str([str(card) for card in self.exhaust_pile]))
