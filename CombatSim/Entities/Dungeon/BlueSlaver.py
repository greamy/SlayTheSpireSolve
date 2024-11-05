import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Weak import Weak
from CombatSim.Entities.Player import Player


class BlueSlaver(Enemy):
    STAB = 0
    RAKE = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Stab(ascension),
                      self.Rake(ascension),
                      ]

        if ascension < 7:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(48, 52), intent_set, ascension, minion=False)
        if ascension < 17:
            self.rake_consec = 3
        else:
            self.rake_consec = 2

    def choose_intent(self):
        if self.intent == self.intent_set[self.STAB] and self.num_consecutive == 3:
            self.intent = self.intent_set[self.RAKE]
        if self.intent == self.intent_set[self.RAKE] and self.num_consecutive == self.rake_consec:
            self.intent = self.intent_set[self.STAB]
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Stab(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 12
            else:
                self.damage = 13
            super().__init__("Stab", self.damage, 1, 0, 60, char.Intent.ATTACK)

    class Rake(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 7
            else:
                self.damage = 8
            if ascension < 17:
                self.weak = 1
            else:
                self.weak = 2

            super().__init__("Rake", self.damage, 1, 0, 40, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)
            listener = Listener(Listener.Event.START_TURN, weak.decrement)
            player.add_listener(listener)
