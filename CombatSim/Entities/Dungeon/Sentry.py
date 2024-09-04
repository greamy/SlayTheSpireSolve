import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Dazed import Dazed
from CombatSim.Entities.Enemy import Enemy


class Sentry(Enemy):
    BEAM = 0
    BOLT = 1

    def __init__(self, ascension: int, act: int,):

        intent_set = [self.Beam(ascension),
                      self.Bolt(ascension),
                      ]
        self.pattern_index = 1
        self.middle = True
        if ascension < 8:
            super().__init__(random.randint(38, 42), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(39, 45), intent_set, ascension, minion=False)

        if self.middle:
            self.pattern = [self.intent_set[self.BEAM], self.intent_set[self.BOLT]]
        else:
            self.pattern = [self.intent_set[self.BOLT], self.intent_set[self.BEAM]]

    def choose_intent(self):
        if self.num_turns == 0 and self.middle:
            self.intent = self.intent_set[self.BEAM]
        elif self.num_turns == 0 and not self.middle:
            self.intent = self.intent_set[self.BOLT]
        elif self.num_turns > 0:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Beam(Intent):
        def __init__(self, ascension: int):
            if ascension < 3:
                self.damage = 9
            else:
                self.damage = 10
            super().__init__("Beam", self.damage, 1, 0, 0, char.Intent.ATTACK)

    class Bolt(Intent):
        def __init__(self, ascension: int):
            if ascension < 18:
                self.dazed = 2
            else:
                self.dazed = 3
            super().__init__("Bolt", 0, 0, 0, 100, char.Intent.DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            for _ in range(self.dazed):
                player.deck.discard_pile.append(Dazed(player))
