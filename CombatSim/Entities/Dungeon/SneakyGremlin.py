import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy



class SneakyGremlin(Enemy):
    PUNCTURE = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Puncture(ascension)]

        if ascension < 7:
            super().__init__(random.randint(10, 14), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(11, 15), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Puncture(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 9
            else:
                self.damage = 10
            super().__init__("Puncture", self.damage, 1, 0, 100, char.Intent.ATTACK)
