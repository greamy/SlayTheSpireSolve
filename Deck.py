# this is the area where you are going to make cards
import random
from Card import Card


class Deck:
    def __init__(self, cards):
        self.deck = cards
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []

    def begin_combat(self):
        self.shuffle()
        self.drawHand(5)

    def shuffle(self):
        for i in range(len(self.deck)):
            self.swap(i, random.randint(0, len(self.deck)-1))

    def swap(self, first, second):
        tmp = self.deck[first]
        self.deck[first] = self.deck[second]
        self.deck[second] = tmp

    # Return a list of length num of cards
    def draw_hand(self, num):
        for i in range(num):
            self.hand.append(self.deck.pop(0))

    def draw(self, amount):
        self.hand.extend([self.deck.pop(0) for i in range(amount)])

    def discard(self, index):
        self.discard_pile.append(self.hand.pop(index))

    def exhaust(self, card):
        pass

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand.clear()
        print("**************** TURN OVER ****************")

    def __str__(self):
        return "Deck:" + str([str(card) for card in self.deck]) + "\nHand: " + str([str(card) for card in self.hand]) \
               + "\nDiscard: " + str([str(card) for card in self.discard_pile]) \
               + "\nExhaust: " + str([str(card) for card in self.exhaust_pile])

