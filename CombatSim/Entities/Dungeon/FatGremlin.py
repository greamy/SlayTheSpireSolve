import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Weak import Weak
from CombatSim.Entities.Status.Frail import Frail


class FatGremlin(Enemy):
    SMASH = 0

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Smash(ascension)]

        if ascension < 7:
            super().__init__(random.randint(13, 17), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(14, 18), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Smash(Intent):
        def __init__(self, ascension: int):
            self.weak = 1
            self.frail = 0
            if ascension < 2:
                self.damage = 4
            else:
                self.damage = 5
            if ascension > 16:
                self.frail = 1
            super().__init__("Stab", self.damage, 1, 0, 100, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            if self.frail > 0:
                frail = Frail(self.frail, player)
                listener = Listener(Listener.Event.START_TURN, frail.decrement)
                player.add_listener(listener)
            weak = Weak(self.weak, player)
            listener = Listener(Listener.Event.START_TURN, weak.decrement)
            player.add_listener(listener)


