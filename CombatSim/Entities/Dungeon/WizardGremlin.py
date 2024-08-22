from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Player import Player


class WizardGremlin(Enemy):
    CHARGING = 0
    ULTIMATE_BLAST = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Charging(ascension), self.UltimateBlast(ascension)]
        self.shieldBashFlag = False

        if ascension < 7:
            super().__init__(random.randint(23, 25), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(22, 26), intent_set, ascension, minion=False)

    def choose_intent(self):
        pass

    def is_valid_intent(self, intent: Intent) -> bool:
        pass

    class Charging(Intent):
        pass