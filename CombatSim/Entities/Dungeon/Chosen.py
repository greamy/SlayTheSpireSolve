import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Dazed import Dazed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Vulnerable import Vulnerable
from CombatSim.Entities.Weak import Weak


class Chosen(Enemy):
    POKE = 0
    ZAP = 1
    DEBILITATE = 2
    DRAIN = 3
    HEX = 4

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Poke(ascension),
                      self.Zap(ascension),
                      self.Debilitate(ascension),
                      self.Drain(ascension),
                      self.Hex(ascension)]
        if ascension < 17:
            self.a17 = False
        else:
            self.a17 = True
        self.pattern = True

        if ascension < 7:
            super().__init__(random.randint(95, 99), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(98, 103), intent_set, ascension, minion=False)
        self.true_pattern = [self.intent_set[self.DEBILITATE], self.intent_set[self.DRAIN]]
        self.false_pattern = [self.intent_set[self.POKE], self.intent_set[self.ZAP]]

    def choose_intent(self):
        if self.num_turns == 0:
            if self.a17:
                self.intent = self.intent_set[self.HEX]
            else:
                self.intent = self.intent_set[self.POKE]
        elif self.num_turns == 1 and not self.a17:
            self.intent = self.intent_set[self.HEX]
        else:
            if self.pattern:
                num = random.randint(0, 100)
                if num < 50:
                    self.intent = self.true_pattern[0]
                    self.pattern = False
                else:
                    self.intent = self.true_pattern[1]
                    self.pattern = False
            else:
                num = random.randint(0, 100)
                if num < 60:
                    self.intent = self.false_pattern[0]
                else:
                    self.intent = self.false_pattern[1]

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Poke(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 5
            else:
                self.damage = 6
            super().__init__("Poke", self.damage, 2, 0, 0, char.Intent.ATTACK)

    class Zap(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 18
            else:
                self.damage = 21
            super().__init__("Zap", self.damage, 1, 0, 0, char.Intent.ATTACK)

    class Debilitate(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 12
            super().__init__("Debilitate", self.damage, 1, 0, 0, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            vuln = Vulnerable(2, player)
            player.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))

    class Drain(Intent):
        def __init__(self, ascension):
            super().__init__("Drain", 0, 0, 0, 0, char.Intent.DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(3, player)
            player.add_listener(Listener(Listener.Event.START_TURN, weak.decrement))
            enemy.damage_dealt_modifier += 3

    class Hex(Intent):
        def __init__(self, ascension):
            super().__init__("Hex", 0, 0, 0, 100, char.Intent.STRONG_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.add_listener(Listener(Listener.Event.SKILL_PLAYED, self.add_dazed))

        def add_dazed(self, player, enemy, enemies, debug):
            player.deck.draw_pile.append(Dazed(player))



