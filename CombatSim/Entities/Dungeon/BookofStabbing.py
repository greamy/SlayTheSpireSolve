import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Wound import Wound
from CombatSim.Entities.Enemy import Enemy


class BookofStabbing(Enemy):
    MULTISTAB = 0
    SINGLESTAB = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.MultiStab(ascension), self.SingleStab(ascension)]

        if ascension < 8:
            super().__init__(random.randint(160, 162), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(168, 172), intent_set, ascension, minion=False)
        self.attacks_done = 0
        self.all_attacks_flag = self.ascension > 17

    def choose_intent(self):
        super().choose_intent()
        if self.intent == self.intent_set[self.MultiStab]:
            self.attacks_done += 1
        elif self.intent == self.intent_set[self.SingleStab] and self.all_attacks_flag:
            self.attacks_done += 1


    def is_valid_intent(self, intent: Intent):
        if self.intent == self.intent_set[self.MultiStab] and self.num_consecutive == 3:
            return False
        elif self.intent == self.intent_set[self.SingleStab]:
            return False
        else:
            return True

    class MultiStab(Intent):
        def __init__(self, ascension:int):
            if ascension < 3:
                self.damage = 6
            else:
                self.damage = 7
            super().__init__("MultiStab", self.damage, 0, 0, 85, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            self.attacks = enemy.attacks_done
            super().play(enemy, enemy_list, player, player_list, debug)

    class SingleStab(Intent):
        def __init__(self, ascension:int):
            if ascension < 3:
                self.damage = 21
            else:
                self.damage = 24
            super().__init__("SingleStab", self.damage, 1, 0, 15, char.Intent.ATTACK)