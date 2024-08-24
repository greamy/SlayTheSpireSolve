from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Player import Player


class FungiBeast(Enemy):
    # Must be ordered based on probability. Lowest to highest.
    GROW = 0
    BITE = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Grow(ascension), self.Bite(ascension)]

        if ascension < 7:
            super().__init__(random.randint(22, 28), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(24, 26), intent_set, ascension, minion=False)

    def choose_intent(self):
        if self.intent == self.intent_set[self.BITE] and self.num_consecutive == 3:
            self.intent = self.intent_set[self.GROW]
        if self.intent == self.intent_set[self.GROW] and self.num_consecutive == 2:
            self.intent = self.intent_set[self.BITE]

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Grow(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.strength = 3
            elif ascension < 17:
                self.strength = 4
            else:
                self.strength = 5
            super().__init__("Grow", 0, 0, 0, 40)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength

    class Bite(Intent):
        def __init__(self, ascension: int):
            super().__init__("Bite", 6, 1, 0, 60)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
