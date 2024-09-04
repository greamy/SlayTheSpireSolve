import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy


class WizardGremlin(Enemy):
    # Must be ordered based on probability. Lowest to highest.
    CHARGING = 0
    ULTIMATE_BLAST = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Charging(ascension), self.UltimateBlast(ascension)]
        self.shieldBashFlag = False
        self.loop = False

        if ascension < 7:
            super().__init__(random.randint(23, 25), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(22, 26), intent_set, ascension, minion=False)

        if ascension < 17:
            self.pattern_index = 0
            self.pattern = [self.intent_set[self.CHARGING], self.intent_set[self.CHARGING],
                            self.intent_set[self.CHARGING], self.intent_set[self.ULTIMATE_BLAST]]
            self.loop = True

    def choose_intent(self):
        if self.num_turns < 2:
            self.intent = self.intent_set[self.CHARGING]
        elif self.num_turns == 2:
            self.intent = self.intent_set[self.ULTIMATE_BLAST]
        elif not self.loop and self.num_turns > 2:
            self.intent = self.intent_set[self.ULTIMATE_BLAST]
        elif self.loop and self.num_turns > 2:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Charging(Intent):
        def __init__(self, ascension: int):
            super().__init__("Charging", 0, 0, 0, 0, char.Intent.UNKNOWN)

    class UltimateBlast(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 25
            else:
                self.damage = 30
            super().__init__("UltimateBlast", self.damage, 1, 0, 100, char.Intent.ATTACK)
