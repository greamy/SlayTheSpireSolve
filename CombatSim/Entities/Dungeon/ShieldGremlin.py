import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy


class ShieldGremlin(Enemy):
    PROTECT = 1
    SHIELDBASH = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.ShieldBash(ascension), self.Protect(ascension)]
        self.shieldBashFlag = False

        if ascension < 7:
            super().__init__(random.randint(12, 15), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(13, 17), intent_set, ascension, minion=False)

    def choose_intent(self):
        if self.shieldBashFlag:
            self.intent = self.intent_set[self.SHIELDBASH]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Protect(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.block = 7
            elif ascension < 17:
                self.block = 8
            else:
                self.block = 11
            super().__init__("Protect", 0, 0, self.block, 100, char.Intent.DEFEND)

        def play(self, enemy, enemy_list, player, player_list, debug):
            if len(enemy_list) > 1:
                not_self_enemy_list = enemy_list.remove(enemy)
                super().play(random.choice(not_self_enemy_list), enemy_list, player, player_list, debug)
            else:
                super().play(enemy, enemy_list, player, player_list, debug)
                enemy.shieldBashFlag = True

    class ShieldBash(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 6
            else:
                self.damage = 8
            super().__init__("ShieldBash", self.damage, 1, 0, 0, char.Intent.ATTACK)
