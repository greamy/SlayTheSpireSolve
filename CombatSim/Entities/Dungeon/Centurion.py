import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy

class Centurion(Enemy):
    SLASH = 0
    FURY = 2
    DEFEND = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Slash(ascension), self.Fury(ascension), self.Defend(ascension)]
        self.Flurry_flag = False
        if ascension < 7:
            super().__init__(random.randint(76, 80), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(78, 83), intent_set, ascension, minion=False)

    def choose_intent(self):
        if self.Flurry_flag:
            self.Fury.probability = 35
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Slash(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 12
            else:
                self.damage = 14
            super().__init__("Slash", self.damage, 1, 0, 65, char.Intent.ATTACK)

    class Defend(Intent):
        def __init__(self, ascension: int):
            if ascension < 17:
                self.block = 15
            else:
                self.block = 20
            super().__init__("Defend", 0, 0, self.block, 35, char.Intent.DEFEND)

        def play(self, enemy, enemy_list, player, player_list, debug):
            if len(enemy_list) > 1:
                not_self_enemy_list = enemy_list.remove(enemy)
                super().play(random.choice(not_self_enemy_list), enemy_list, player, player_list, debug)
            else:
                super().play(enemy, enemy_list, player, player_list, debug)
                self.probability = 0
                enemy.flurry_flag = True

    class Fury(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 6
            else:
                self.damage = 7
            super().__init__("Fury", self.damage, 3, 0, 0, char.Intent.ATTACK)