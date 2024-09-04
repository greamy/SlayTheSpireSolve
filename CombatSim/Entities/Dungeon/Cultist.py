import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player


class Cultist(Enemy):
    INCANTATION = 0
    DARKSTRIKE = 1

    def __init__(self, ascension: int, act: int):
        intent_set = [
            self.Incantation(ascension),
            self.DarkStrike(ascension)
        ]
        if ascension >= 7:
            super().__init__(random.randint(48, 54), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(50, 56), intent_set, ascension, minion=False)


    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.INCANTATION]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        # 0 = First Turn
        if self.num_turns > 0 and self.intent == self.intent_set[self.INCANTATION]:
            return False
        return True

    class Incantation(Intent):
            def __init__(self, ascension: int):
                super().__init__("Incantation", 0, 0, 0, 0, char.Intent.BUFF)
                self.ritual = 3
                if ascension >= 2:
                    self.ritual = 4
                elif ascension >= 17:
                    self.ritual = 5
                self.listener = Listener(Listener.Event.END_TURN, self.do_ritual)

            def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
                super().play(enemy, enemy_list, player, player_list, debug)
                enemy.add_listener(self.listener)

            def do_ritual(self, enemy: Enemy, player: Player, player_list: list[Player], debug: bool):
                enemy.damage_dealt_modifier += self.ritual

    class DarkStrike(Intent):
        def __init__(self, ascension: int):
            super().__init__("DarkStrike", 6, 1, 0, 100, char.Intent.ATTACK)

