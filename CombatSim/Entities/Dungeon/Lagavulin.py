import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy

from CombatSim.Entities.Status.Metallicize import Metallicize

class Lagavulin(Enemy):
    ATTACK = 1
    SIPHONSOUL = 0
    SLEEP = 2
    def __init__(self, ascension: int, act: int):

        intent_set = [
                      self.SiphonSoul(ascension),
                      self.Attack(ascension),
                      self.Sleep(ascension)]

        self.sleeping = True

        if ascension < 8:
            super().__init__(random.randint(109, 111), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(112, 115), intent_set, ascension, minion=False)

        self.start_health = self.health
        self.pattern_index = 0
        self.pattern = [self.intent_set[self.ATTACK], self.intent_set[self.ATTACK],
                        self.intent_set[self.SIPHONSOUL]]

        self.metallicize_amount = 8
        self.metallicize = Metallicize(self.metallicize_amount, self)
        self.block = self.metallicize_amount

    def take_damage(self, amount):
        lost_health = super().take_damage(amount)
        if self.health < self.start_health :
            self.sleeping = False
            self.metallicize.remove()
        return lost_health

    def choose_intent(self):
        if self.num_turns < 3 and self.sleeping:
            self.intent = self.intent_set[self.SLEEP]
        else:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Sleep(Intent):
        def __init__(self, ascension: int):
            super().__init__("Sleep", 0, 0, 0, 100, char.Intent.SLEEP)

        def play(self, enemy, enemy_list, player, player_list, debug):
            pass


    class Attack(Intent):
        def __init__(self, ascension: int):
            if ascension < 3:
                self.damage = 18
            else:
                self.damage = 20
            super().__init__("Attack", self.damage, 1, 0, 0, char.Intent.ATTACK)

    class SiphonSoul(Intent):
        def __init__(self, ascension: int):
            if ascension < 18:
                self.debuff = 1
            else:
                self.debuff = 2
            super().__init__("SiphonSoul", 0, 0, 0, 0, char.Intent.STRONG_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            player.block_modifier -= self.debuff
            player.damage_dealt_modifier -= self.debuff


