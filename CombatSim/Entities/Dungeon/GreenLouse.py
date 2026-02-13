import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Weak import Weak
from CombatSim.Actions.Listener import Listener


class GreenLouse(Enemy):
    SPITWEB = 0
    BITE = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.SpitWeb(ascension), self.Bite(ascension)]
        if ascension < 2:
            self.D = random.randint(5, 7)
        else:
            self.D = random.randint(6, 8)

        if ascension < 7:
            super().__init__(random.randint(11, 17), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(12, 18), intent_set, ascension, minion=False)

        if ascension < 7:
            self.curl_up = random.randint(3, 7)
            self.spit_consec = 2
        elif ascension < 17:
            self.curl_up = random.randint(4, 8)
            self.spit_consec = 2
        else:
            self.curl_up = random.randint(9, 12)
            self.spit_consec = 2
        self.curl_up_used = False

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.intent == self.intent_set[self.SPITWEB] and self.num_consecutive == self.spit_consec:
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

    class SpitWeb(Intent):
        def __init__(self, ascension):
            self.weak = 2
            super().__init__("SpitWeb", 0, 0, 0, 25, char.Intent.DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)
