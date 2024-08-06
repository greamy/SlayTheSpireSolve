from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random


class JawWorm(Enemy):
    CHOMP = 0
    THRASH = 1
    BELLOW = 2

    def __init__(self, ascension: int):
        intent_set = [
            Intent("Chomp", 12, 1, 0, 25),
            Intent("Thrash", 7, 1, 5, 30),
            self.Bellow(ascension)
        ]
        if ascension >= 7:
            super().__init__(random.randint(42, 46), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(40, 44), intent_set, ascension, minion=False)

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.CHOMP]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if ((intent == self.intent_set[self.BELLOW] or intent == self.intent_set[self.CHOMP])
                and self.num_consecutive == 2):
            return False
        if intent == self.intent_set[self.THRASH] and self.num_consecutive == 3:
            return False

        return True

    class Bellow(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.block = 6
                self.strength = 3
            elif ascension < 17:
                self.block = 6
                self.strength = 4
            else:
                self.block = 9
                self.strength = 5

            super().__init__("Bellow", 0, 0, self.block, 45)

        def play(self, enemy, player, player_list, debug):
            super().play(enemy, player, player_list, debug)
            enemy.damage_dealt_modifier += self.strength
