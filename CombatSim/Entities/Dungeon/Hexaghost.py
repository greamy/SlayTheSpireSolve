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
        self.pattern_index = 1
        self.pattern = [self.intent_set[self.SEAR], self.intent_set[self.TACKLE], self.intent_set[self.SEAR],
                        self.intent_set[self.INFLAME], self.intent_set[self.TACKLE], self.intent_set[self.SEAR],
                        self.intent_set[self.INFERNO]]

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.ACTIVATE]
        elif self.num_turns == 1:
            self.intent = self.intent_set[self.DIVIDER]
        else:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Activate(Intent):
        def __init__(self, ascension):
            super().__init__("Activate", 0, 0, 0, 0)

    class Divider(Intent):
        def __init__(self, ascension):
            super().__init__("Divider", 1, 6, 0, 1)

        def play(self, enemy, enemy_list, player, player_list, debug):
            self.damage = (floor(player.health / 12) + 1)
            super().play(enemy, enemy_list, player, player_list, debug)

    class Inferno(Intent):
        def __init__(self, ascension):
            if ascension < 4:
                self.damage = 2
            else:
                self.damage = 3
            super().__init__("Inferno", self.damage, 6, 0, 2)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.extend([Burn(player) for _ in range(3)])
            if not enemy.first_inferno:
                for card in player.deck.discard_pile:
                    if card.name == "Burn":
                        card.upgrade()
                for card in player.deck.draw_pile:
                    if card.name == "Burn":
                        card.upgrade()
                enemy.first_inferno = True

    class Sear(Intent):
        def __init__(self, ascension: int):
            if ascension < 19:
                self.burn_amount = 1
            else:
                self.burn_amount = 2
            super().__init__("Sear", 6, 1, 0, 3)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.extend([Burn(player) for _ in range(self.burn_amount)])

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
            super().__init__("Inflame", 0, 0, 12, 90)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength


