from math import floor

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Burn import Burn
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
import random


from CombatSim.Entities.Player import Player


class Hexaghost(Enemy):
    ACTIVATE = 0
    DIVIDER = 1
    INFERNO = 2
    SEAR = 3
    TACKLE = 4
    INFLAME = 5

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Activate(ascension),
                      self.Divider(ascension),
                      self.Inferno(ascension),
                      self.Sear(ascension),
                      self.Tackle(ascension),
                      self.Inflame(ascension)
                      ]

        if ascension < 9:
            super().__init__(250, intent_set, ascension, minion=False)
        else:
            super().__init__(264, intent_set, ascension, minion=False)
        self.first_inferno = False
    def choose_intent(self):
        pass

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Activate(Intent):
        def __init__(self, ascension):
            super().__init__("Activate", 0, 0, 0, 0)

    class Divider(Intent):
        def __init__(self, ascension):
            super().__init__("Divider", self.damage, 6, 0, 1)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            self.damage = (floor(player.health/12) + 1)

    class Inferno(Intent):
        def __init__(self, ascension):
            if ascension < 4:
                self.damage = 2
            else:
                self.damage = 3
            super().__init__("Inferno", self.damage, 6, 0, 2)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.append(Burn(player) for _ in range(3))

    class Sear(Intent):
        def __init__(self, ascension: int):
            if ascension < 19:
                self.burn_amount = 1
            else:
                self.burn_amount = 2
            super().__init__("Sear", 6, 1, 0, 3)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.append(Burn(player) for _ in range(self.burn_amount))

    class Tackle(Intent):
        def __init__(self, ascension):
            if ascension < 4:
                self.damage = 5
            else:
                self.damage = 6
            super().__init__("Tackle", self.damage, 2, 0, 4)

    class Inflame(Intent):
        def __init__(self, ascension):
            if ascension < 19:
                self.strength = 2
            else:
                self.strength = 3
            super().__init__("Inflame", 0, 0, 12, 5)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength


