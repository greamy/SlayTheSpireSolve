import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Frail import Frail
from CombatSim.Entities.PlatedArmor import PlatedArmor
from CombatSim.Entities.Player import Player


class ShelledParasite(Enemy):
    STUNNED = 0
    FELL = 0+1
    DOUBLESTRIKE = 1+1
    SUCK = 2+1

    def __init__(self, ascension: int, act: int):
        intent_set = [
            self.Stunned(ascension),
            self.Fell(ascension),
            self.DoubleStrike(ascension),
            self.Suck(ascension)
        ]

        if ascension < 17:
            self.a17 = False
        else:
            self.a17 = True
        if ascension >= 7:
            super().__init__(random.randint(68, 72), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(70, 75), intent_set, ascension, minion=False)
        self.plated_armor = 14
        PlatedArmor(self.plated_armor, self)


    def choose_intent(self):
        if self.num_turns == 0:
            if self.a17:
                self.intent = self.intent_set[self.FELL]
            else:
                num = random.randint(0, 100)
                if num < 50:
                    self.intent = self.intent_set[self.SUCK]
                else:
                    self.intent = self.intent_set[self.DOUBLESTRIKE]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.intent == self.intent_set[self.FELL] and self.num_consecutive == 2:
            return False
        elif self.intent == self.intent_set[self.DOUBLESTRIKE] and self.num_consecutive == 3:
            return False
        elif self.intent == self.intent_set[self.SUCK] and self.num_consecutive == 3:
            return False
        else:
            return True

    class Stunned(Intent):
        def __init__(self, ascension):
            super().__init__("Stunned", 0, 0, 0, 0, char.Intent.STUN)

    class DoubleStrike(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 6
            else:
                self.damage = 7
            super().__init__("DoubleStrike", self.damage, 2, 0, 40, char.Intent.ATTACK)

    class Suck(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 12
            super().__init__("Suck", self.damage, 1, 0, 40, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            start_player_health = player.health
            super().play(enemy, enemy_list, player, player_list, debug)
            end_player_health = player.health
            enemy.health += start_player_health - end_player_health

    class Fell(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 18
            else:
                self.damage = 21
            super().__init__("Fell", self.damage, 1, 0, 20, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            frail = Frail(2, player)
            player.add_listener(Listener(Listener.Event.START_TURN, frail.decrement))
