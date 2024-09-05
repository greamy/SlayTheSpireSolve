import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy


class Looter(Enemy):
    MUG = 0
    LUNGE = 1
    SMOKEBOMB = 2
    ESCAPE = 3

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Mug(ascension),
                      self.Lunge(ascension),
                      self.SmokeBomb(ascension),
                      self.Escape(ascension)]

        self.next_intent = None

        if ascension < 7:
            super().__init__(random.randint(44, 48), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        self.gold_stolen = 0
        if ascension < 17:
            self.thievery = 15
        else:
            self.thievery = 20