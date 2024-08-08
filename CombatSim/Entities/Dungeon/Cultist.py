from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
import random

class Cultist(Enemy):
    INCANTATION = 0
    DARKSTRIKE = 1

    def __init__(self, ascension: int):
        intent_set = [
            self.Incantation(ascension), self.DarkStrike(ascension),]
        if ascension >= 7:
            super().__init__(random.randint(48, 54), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(50, 56), intent_set, ascension, minion=False)


    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.Incantation]
        else:
            super().choose_intent()



    class Incantation(Intent):
            def __init__(self, ascension: int):
                super().__init__("Incantation", 0, 0, 0, 0)

            def play(self, enemy, player, player_list, debug):
                super().play(enemy, player, player_list, debug)
                self.ritual

