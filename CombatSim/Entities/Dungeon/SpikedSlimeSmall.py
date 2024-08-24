from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Player import Player


class SpikedSlimeSmall(Enemy):
    # Must be ordered based on probability. Lowest to highest.
    TACKLE = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Tackle(ascension)]

        if ascension < 7:
            super().__init__(random.randint(10, 14), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(11, 15), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Tackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 5
            else:
                self.damage = 6
            super().__init__("Tackle", self.damage, 1, 0, 100)
