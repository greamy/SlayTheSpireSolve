import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy


class Looter(Enemy):
    MUG = 0
    ESCAPE = 1
    LUNGE = 2
    SMOKEBOMB = 3


    def __init__(self, ascension: int, act: int):

        intent_set = [self.Mug(ascension),
                      self.Escape(ascension),
                      self.Lunge(ascension),
                      self.SmokeBomb(ascension),
                      ]

        self.next_intent = None

        if ascension < 7:
            super().__init__(random.randint(44, 48), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        self.gold_stolen = 0
        if ascension < 17:
            self.thievery = 15
        else:
            self.thievery = 20

        self.listener = Listener(Listener.Event.TAKEN_DAMAGE, self.return_gold)
        self.add_listener(self.listener)
    def return_gold(self, enemy, player, player_list, debug):
        if enemy.health <= 0:
            player.gold += enemy.gold_stolen

    def choose_intent(self):
        if self.num_turns == 1 or self.num_turns == 0:
            self.intent = self.intent_set[self.MUG]
        if self.next_intent is not None:
            self.intent = self.next_intent
            self.next_intent = None
        else:
            super().choose_intent()

        if self.num_turns == 2 and self.intent == self.intent_set[self.LUNGE]:
            self.next_intent = self.intent_set[self.SMOKEBOMB]
        elif self.intent == self.intent_set[self.SMOKEBOMB]:
            self.next_intent = self.intent_set[self.ESCAPE]

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Mug(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 11
            super().__init__("Mug", self.damage, 1, 0, 0, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.gold -= enemy.thievery
            enemy.gold_stolen += enemy.thievery

    class Lunge(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 12
            else:
                self.damage = 14
            super().__init__("Lunge", self.damage, 1, 0, 50, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.gold -= enemy.thievery
            enemy.gold_stolen += enemy.thievery

    class SmokeBomb(Intent):
        def __init__(self, ascension: int):
            super().__init__("SmokeBomb", 0, 0, 6, 50, char.Intent.DEFEND)

    class Escape(Intent):
        def __init__(self, ascension: int):
            super().__init__("Escape", 0, 0, 0, 0, char.Intent.ESCAPE)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().__init__(enemy, enemy_list, player, player_list, debug, char.Intent.ESCAPE)
            enemy_list.remove(enemy)

