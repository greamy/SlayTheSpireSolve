import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy


class Byrd(Enemy):
    STUNNED = 0
    FLY = 1
    HEADBUTT = 2
    SWOOP = 3
    CAW = 4
    PECK = 5

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Fly(ascension),
                      self.Headbutt(ascension),
                      self.Swoop(ascension),
                      self.Caw(ascension),
                      self.Peck(ascension),
                      self.Stunned(ascension)]

        if ascension < 7:
            super().__init__(random.randint(25, 31), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(26, 33), intent_set, ascension, minion=False)
        self.flying = True
        if ascension < 17:
            self.flying_amount = 3
        else:
            self.flying_amount = 4
        self.ground_pattern = [self.intent_set[self.HEADBUTT], self.intent_set[self.FLY]]
        self.ground_pattern_index = 0

    def take_damage(self, amount):
        lost_health = False
        if self.flying:
            amount = amount/2
            lost_health = super().take_damage(amount)
            self.flying_amount -= 1
            if self.flying_amount <= 0:
                self.flying = False
                self.intent = self.intent_set[self.STUNNED]
        return lost_health

    def choose_intent(self):
        if self.num_turns == 0:
            choice = random.randint(0, 1000)
            if choice <= 625:
                self.intent = self.intent_set[self.PECK]
            else:
                self.intent = self.intent_set[self.CAW]
        elif not self.flying:
            if self.ground_pattern_index >= len(self.ground_pattern):
                self.ground_pattern_index = 0
            self.intent = self.ground_pattern[self.ground_pattern_index]
            self.ground_pattern_index += 1
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.intent == self.intent_set[self.PECK] and self.num_consecutive == 3:
            return False
        elif self.intent == self.intent_set[self.CAW] and self.num_consecutive == 2:
            return False
        elif self.intent == self.intent_set[self.SWOOP] and self.num_consecutive == 2:
            return False
        else:
            return True

    class Stunned(Intent):
        def __init__(self, ascension):
            super().__init__("Stunned", 0, 0, 0, 0, char.Intent.STUN)

    class Fly(Intent):
        def __init__(self, ascension):
            super().__init__("Fly", 0, 0, 0, 0, char.Intent.BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.flying += 4

    class Headbutt(Intent):
        def __init__(self, ascension):
            super().__init__("Headbutt", 3, 1, 0, 0, char.Intent.ATTACK)

    class Swoop(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 12
            else:
                self.damage = 14
            super().__init__("Swoop", self.damage, 1, 0, 20, char.Intent.ATTACK)

    class Caw(Intent):
        def __init__(self, ascension):
            super().__init__("Caw", 0, 0, 0, 30, char.Intent.BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += 1

    class Peck(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.attacks = 5
            else:
                self.attacks = 6
            super().__init__("Peck", 1, self.attacks, 0, 50, char.Intent.ATTACK)
