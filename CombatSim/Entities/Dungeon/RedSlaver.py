import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy

from CombatSim.Entities.Status.Vulnerable import Vulnerable



class RedSlaver(Enemy):
    ENTANGLE = 0
    STAB = 1
    SCRAPE = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Stab(ascension),
                      self.Scrape(ascension),
                      self.Entangle(ascension)
                      ]

        self.entangled_used = False
        self.intent_pattern_index = 1
        if ascension < 7:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(48, 52), intent_set, ascension, minion=False)
        if ascension < 17:
            self.intent_pattern = [self.intent_set[self.SCRAPE], self.intent_set[self.SCRAPE],
                                   self.intent_set[self.STAB]]
            self.scrape_num_consec = 3
        else:
            self.intent_pattern = [self.intent_set[self.SCRAPE], self.intent_set[self.STAB]]
            self.scrape_num_consec = 2

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.STAB]
        elif not self.entangled_used:
            num = random.randint(1, 4)
            if num == 1:
                self.intent = self.intent_set[self.ENTANGLE]
            else:
                if self.intent_pattern_index >= len(self.intent_pattern):
                    self.intent_pattern_index = 1
                self.intent = self.intent_pattern[self.intent_pattern_index]
                self.intent_pattern_index += 1
        elif self.entangled_used:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.entangled_used:
            if self.intent == self.intent_set[self.SCRAPE] and self.num_consecutive == self.scrape_num_consec:
                return False
            elif self.intent == self.intent_set[self.STAB] and self.num_consecutive == 3:
                return False
            else:
                return True

    class Stab(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 13
            else:
                self.damage = 14
            super().__init__("Stab", self.damage, 1, 0, 45, char.Intent.ATTACK)

    class Scrape(Intent):
        def __init__(self, ascension: int):

            if ascension < 2:
                self.damage = 8
            else:
                self.damage = 9
            if ascension < 17:
                self.vuln = 1
            else:
                self.vuln = 2
            super().__init__("Scrape", self.damage, 1, 0, 55, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            vuln = Vulnerable(self.vuln, player)

    class Entangle(Intent):
        def __init__(self, ascension: int):
            super().__init__("Entangle", 0, 0, 0, 0, char.Intent.STRONG_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
