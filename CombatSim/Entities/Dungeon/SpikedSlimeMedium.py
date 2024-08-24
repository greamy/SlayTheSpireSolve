from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Slimed import Slimed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Frail import Frail
from CombatSim.Entities.Player import Player


class SpikedSlimeMedium(Enemy):
    # Must be ordered based on probability. Lowest to highest.
    FLAMETACKLE = 0
    LICK = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.FlameTackle(ascension), self.Lick(ascension)]

        if ascension < 7:
            super().__init__(random.randint(28, 32), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(29, 34), intent_set, ascension, minion=False)

        if ascension < 17:
            self.lick_consec = 2
        else:
            self.lick_consec = 3

    def choose_intent(self):
        if self.intent == self.intent_set[self.FLAMETACKLE] and self.num_consecutive == 3:
            self.intent = self.intent_set[self.LICK]
        elif self.intent == self.intent_set[self.LICK] and self.num_consecutive == self.lick_consec:
            self.intent = self.intent_set[self.FLAMETACKLE]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class FlameTackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 8
            else:
                self.damage = 10
            super().__init__("Tackle", self.damage, 1, 0, 30)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.append(Slimed(player))

    class Lick(Intent):
        def __init__(self, ascension: int):
            self.frail = 1
            super().__init__("Lick", 0, 0, 0, 70)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            frail = Frail(self.frail, player)
            listener = Listener(Listener.Event.START_TURN, frail.decrement)
            player.add_listener(listener)
