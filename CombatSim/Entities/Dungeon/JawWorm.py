import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy

from CombatSim.Entities.Player import Player


class JawWorm(Enemy):
    CHOMP = 0
    THRASH = 1
    BELLOW = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Chomp(ascension),
                      self.Thrash(ascension),
                      self.Bellow(ascension)]

        self.third_act = False
        if act == 3:
            self.third_act = True
        if ascension < 7:
            super().__init__(random.randint(40, 44), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(42, 46), intent_set, ascension, minion=False)

        if act == 3:
            self.damage_dealt_modifier += self.intent_set[self.BELLOW].strength
            self.block += self.intent_set[self.BELLOW].block

    def choose_intent(self):
        if self.num_turns == 0 and not self.third_act:
            self.intent = self.intent_set[self.CHOMP]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if ((intent == self.intent_set[self.BELLOW] or intent == self.intent_set[self.CHOMP])
                and self.num_consecutive == 2):
            return False
        if intent == self.intent_set[self.THRASH] and self.num_consecutive == 3:
            return False

        return True

    class Bellow(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.block = 6
                self.strength = 3
            elif ascension < 17:
                self.block = 6
                self.strength = 4
            else:
                self.block = 9
                self.strength = 5

            super().__init__("Bellow", 0, 0, self.block, 45, char.Intent.DEFEND_BUFF)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength

    class Chomp(Intent):
        def __init__(self, ascension: int):
            if ascension > 2:
                self.damage = 12
            else:
                self.damage = 11
            super().__init__("Chomp", self.damage, 1, 0, 25, char.Intent.ATTACK)

    class Thrash(Intent):
        def __init__(self, ascension: int):
            super().__init__("Thrash", 7, 1, 5, 30, char.Intent.ATTACK_DEFEND)
