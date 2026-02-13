import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Frail import Frail


class SphericGuardian(Enemy):
    ACTIVATE = 0
    AD = 1
    SLAM = 2
    HARDEN = 3

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Activate(ascension),
                      self.Ad(ascension),
                      self.Slam(ascension),
                      self.Harden(ascension)]
        self.barricade = True

        super().__init__(20, intent_set, ascension, minion=False)
        self.block += 40
        self.pattern = [self.intent_set[self.SLAM], self.intent_set[self.HARDEN]]
        self.pattern_index = 0

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.ACTIVATE]
        elif self.num_turns == 1:
            self.intent = self.intent_set[self.AD]
        else:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent_set = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Slam(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 11
            super().__init__("Slam", self.damage, 2, 0, 0, char.Intent.ATTACK)

    class Activate(Intent):
        def __init__(self, ascension):
            if ascension < 17:
                self.block = 25
            else:
                self.block = 35
            super().__init__("Activate", 0, 0, self.block, 0, char.Intent.DEFEND)

    class Harden(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 11
            super().__init__("Harden", self.damage, 1, 15, 0, char.Intent.ATTACK_DEFEND)

    class Ad(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 11
            super().__init__("Ad", self.damage, 1, 0, 100, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            frail = Frail(5, player)