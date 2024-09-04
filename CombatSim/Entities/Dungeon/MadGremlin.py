import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy


class MadGremlin(Enemy):
    SCRATCH = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Scratch(ascension)]

        if ascension < 7:
            super().__init__(random.randint(20, 24), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(21, 25), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Scratch(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 4
            else:
                self.damage = 5
            super().__init__("Scratch", self.damage, 1, 0, 100, char.Intent.ATTACK)
