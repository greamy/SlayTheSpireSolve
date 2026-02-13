import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy

from CombatSim.Entities.Status.Vulnerable import Vulnerable


class GremlinNob(Enemy):
    BELLOW = 0
    SKULLBASH = 1
    RUSH = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Bellow(ascension),
                      self.SkullBash(ascension),
                      self.Rush(ascension),
                      ]

        if ascension < 8:
            super().__init__(random.randint(82, 86), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(85, 90), intent_set, ascension, minion=False)
        self.do_pattern = False
        if ascension < 18:
            self.enrage = 2
        else:
            self.enrage = 3
            self.do_pattern = True
            self.pattern_index = 0
            self.pattern = [self.intent_set[self.SKULLBASH], self.intent_set[self.RUSH], self.intent_set[self.RUSH]]

    def is_alive(self):
        alive = super().is_alive()
        if not alive and self.intent_set[self.BELLOW].player is not None:
            self.intent_set[self.BELLOW].remove_listener()
        return alive

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.BELLOW]
        elif self.num_turns > 0 and self.intent == self.intent_set[self.RUSH] and self.num_consecutive == 3\
                and not self.do_pattern:
            self.intent = self.intent_set[self.SKULLBASH]
        elif self.num_turns > 0 and self.intent == self.intent_set[self.RUSH] and self.num_consecutive == 3\
                and self.do_pattern:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Bellow(Intent):
        def __init__(self, ascension):
            super().__init__("Bellow", 0, 0, 0, 0, char.Intent.DEBUG)
            self.player = None
            self.listener = Listener(Listener.Event.SKILL_PLAYED, self.gain_strength)

        def play(self, enemy, enemy_list, player, player_list, debug):
            player.add_listener(self.listener)
            self.player = player

        def gain_strength(self, player, enemy, enemies, debug):
            enemy.damage_dealt_modifier += enemy.enrage

        def remove_listener(self):
            self.player.remove_listener(self.listener)

    class Rush(Intent):
        def __init__(self, ascension: int):
            if ascension < 3:
                self.damage = 14
            else:
                self.damage = 16
            super().__init__("Rush", self.damage, 1, 0, 67, char.Intent.ATTACK)

    class SkullBash(Intent):
        def __init__(self, ascension):
            self.vulnerable = 2
            if ascension < 3:
                self.damage = 6
            else:
                self.damage = 8
            super().__init__("SkullBash", self.damage, 1, 0, 33, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            vuln = Vulnerable(self.vulnerable, player)
