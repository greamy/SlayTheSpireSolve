from math import floor

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Burn import Burn
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
import random


from CombatSim.Entities.Player import Player
from CombatSim.Entities.Vulnerable import Vulnerable
from CombatSim.Entities.Weak import Weak


class Guardian(Enemy):
    CHARGINGUP = 0
    FIERCEBASH = 1
    VENTSTEAM = 2
    WHIRLWIND = 3
    DEFENSIVEMODE = 4
    ROLLATTACK = 5
    TWINSLAM = 6

    def __init__(self, ascension: int, act: int):

        intent_set = [self.ChargingUp(ascension),
                      self.FierceBash(ascension),
                      self.VentSteam(ascension),
                      self.Whirlwind(ascension),
                      self.DefensiveMode(ascension),
                      self.RollAttack(ascension),
                      self.TwinSlam(ascension)
                      ]

        if ascension < 9:
            super().__init__(240, intent_set, ascension, minion=False)
        else:
            super().__init__(254, intent_set, ascension, minion=False)

    def choose_intent(self):
        pass

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class ChargingUp(Intent):
        def __init__(self, ascension):
            super().__init__("ChargingUp", 0, 0, 9, 1)

    class FierceBash(Intent):
        def __init__(self, ascension):
            if ascension < 4:
                self.damage = 32
            else:
                self.damage = 36
            super().__init__("FierceBash", self.damage, 1, 0, 2)

    class VentSteam(Intent):
        def __init__(self, ascension):
            self.weak = 2
            self.vulnerable = 2
            super().__init__("VentSteam", 0, 0, 0, 3)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)
            vuln = Vulnerable(self.vulnerable, player)
            player.add_listener(Listener(Listener.Event.START_TURN, weak.decrement))
            player.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))

    class Whirlwind(Intent):
        def __init__(self, ascension):
            super().__init__("Whirlwind", 5, 4, 9, 4)

    class DefensiveMode(Intent):
        def __init__(self, ascension):
            super().__init__("DefensiveMode", 0, 0, 0, 5)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)

    class RollAttack(Intent):
        def __init__(self, ascension):
            if ascension < 4:
                self.damage = 9
            else:
                self.damage = 10
            super().__init__("RollAttack", self.damage, 1, 0, 6)

    class TwinSlam(Intent):
        def __init__(self, ascension):
            super().__init__("TwinSlam", 8, 2, 0, 7)
