import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Wound import Wound
from CombatSim.Entities.Enemy import Enemy


class Taskmaster(Enemy):
    SCOURINGWHIP = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.ScouringWhip(ascension)]

        if ascension < 8:
            super().__init__(random.randint(54, 60), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(57, 64), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class ScouringWhip(Intent):
        def __init__(self, ascension: int):
            self.damage = 7
            self.strength = 0
            if ascension < 3:
                self.wounds_added = 1
            elif ascension < 18:
                self.wounds_added = 2
            else:
                self.wounds_added = 3
                self.strength = 1

            super().__init__("Scouring Whip", self.damage, 1, 0, 100, char.Intent.ATTACK)

        def play(self, enemy, enemy_list, player, player_list, debug):
            player.deck.discard_pile.extend([Wound(player) for _ in range(self.wounds_added)])
            super().play(enemy, enemy_list, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength
