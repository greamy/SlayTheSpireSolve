import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy


class ShieldGremlin(Enemy):
    GROW = 0
    BITE = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Grow(ascension), self.Bite(ascension)]
        if ascension < 2:
            self.D = random.randint(5, 7)
        else:
            self.D = random.randint(6,8)

        if ascension < 7:
            super().__init__(random.randint(10, 15), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(11, 16), intent_set, ascension, minion=False)

        if ascension < 7:
            self.curl_up = random.randint(3, 7)
            self.grow_consec = 2
        elif ascension < 17:
            self.curl_up = random.randint(4, 8)
            self.grow_consec = 2
        else:
            self.curl_up = random.randint(9, 12)
            self.grow_consec = 2
        self.curl_up_used = False

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.intent == self.intent_set[self.GROW] and self.num_consecutive == self.grow_consec:
            return False
        elif self.intent == self.intent_set[self.BITE] and self.num_consecutive == 3:
            return False
        else:
            return True

    def take_damage(self, amount):
        super().take_damage(amount)
        if not self.curl_up_used:
            self.block += self.curl_up
            self.curl_up_used = True

    class Bite(Intent):
        def __init__(self, ascension):
            super().__init__("Bite", 1, 1, 0, 75, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            self.damage = enemy.D
            super().play(enemy, enemy_list, player, player_list, debug)

    class Grow(Intent):
        def __init__(self, ascension):
            if ascension < 17:
                self.strength_gain = 3
            else:
                self.strength_gain = 4
            super().__init__("Grow", 0, 0, 0, 25, char.Intent.ATTACK_BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength_gain

