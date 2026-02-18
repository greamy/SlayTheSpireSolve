import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Vulnerable import Vulnerable


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

        self.listener = Listener(Listener.Event.TAKEN_DAMAGE, self.death_vuln)
        self.vuln_duration = 2
    def death_vuln(self, enemy, player, player_list, debug):
        if enemy.health <= 0:
            Vulnerable(player, enemy.vuln_duration )

    def choose_intent(self):
        if self.intent == self.intent_set[self.BITE] and self.num_consecutive == 3:
            self.intent = self.intent_set[self.GROW]
        elif self.intent == self.intent_set[self.GROW] and self.num_consecutive == 2:
            self.intent = self.intent_set[self.BITE]
        else:
            super().choose_intent()

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
            super().__init__("Grow", 0, 0, 0, 40, char.Intent.BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength

    class Bite(Intent):
        def __init__(self, ascension: int):
            super().__init__("Bite", 6, 1, 0, 60, char.Intent.ATTACK)

