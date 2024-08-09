from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Player import Player


class Looter(Enemy):
    MUG = 0
    LUNGE = 1
    SMOKEBOMB = 2
    ESCAPE = 3

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Mug(ascension),
                      self.Lunge(ascension),
                      self.SmokeBomb(ascension),
                      self.Escape]

        if ascension < 7:
            super().__init__(random.randint(44, 48), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        self.gold_stolen = 0
        if ascension < 17:
            self.thievery = 15
        else:
            self.thievery = 20

    def choose_intent(self):
        if self.num_turns == 1 and self.num_turns == 0:
            self.intent = self.intent_set[self.MUG]
        else:
            super().choose_intent()




    class Mug(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 11
            super().__init__("Mug", self.damage, 1, 0, 0)



    class Lunge(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 12
            else:
                self.damage = 14
            super().__init__("Lunge", self.damage, 1, 0, 50)

    class SmokeBomb(Intent):
        def __init__(self, ascension: int):
            super().__init__("SmokeBomb", 0, 0, 6, 50)

