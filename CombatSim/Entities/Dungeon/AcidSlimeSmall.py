import random

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Weak import Weak


class AcidSlimeSmall(Enemy):
    LICK = 0
    TACKLE = 1

    def __init__(self, ascension: int, act: int):
        intent_set = [
            self.Lick(),
            self.Tackle(ascension)
        ]
        if ascension >= 17:
            self.start_intent = intent_set[self.LICK]
        else:
            self.start_intent = random.choice(intent_set)

        if ascension < 7:
            super().__init__(random.randint(8, 12), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(9, 13), intent_set, ascension, minion=False)

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.start_intent
        else:
            # Alternate moves after the first move
            if self.intent == self.intent_set[self.LICK]:
                self.intent = self.intent_set[self.TACKLE]
            else:
                self.intent = self.intent_set[self.LICK]

    def is_valid_intent(self, intent: Intent) -> bool:

        return True

    class Lick(Intent):
        def __init__(self):
            super().__init__("Lick", 0, 0, 0, 50)
            self.weak = 1

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)
            listener = Listener(Listener.Event.START_TURN, weak.decrement)
            player.add_listener(listener)

    class Tackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 3
            else:
                self.damage = 4

            super().__init__("Tackle", self.damage, 1, 0, 50)
