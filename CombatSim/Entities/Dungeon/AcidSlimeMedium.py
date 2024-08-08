import random

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Slimed import Slimed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Weak import Weak


class AcidSlimeMedium(Enemy):
    LICK = 0
    TACKLE = 1
    CORROSIVE_SPIT = 2

    def __init__(self, ascension: int, act: int):
        intent_set = [
            self.Lick(ascension),
            self.Tackle(ascension),
            self.CorrosiveSpit(ascension)
        ]
        self.ascension = ascension

        if ascension < 7:
            super().__init__(random.randint(28, 32), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(29, 34), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.ascension < 17:
            if (intent == self.intent_set[self.TACKLE] and self.num_consecutive == 2):
                return False
            if (intent == self.intent_set[self.CORROSIVE_SPIT] or intent == self.intent_set[self.LICK]) and self.num_consecutive == 3:
                return False
        else:
            if (intent == self.intent_set[self.LICK] and self.num_consecutive == 2):
                return False
            if (intent == self.intent_set[self.CORROSIVE_SPIT] or intent == self.intent_set[self.TACKLE]) and self.num_consecutive == 3:
                return False

        return True
    class Lick(Intent):
        def __init__(self, ascension: int):
            if ascension < 17:
                self.probability = 30
            else:
                self.probability = 20
            super().__init__("Lick", 0, 0, 0, self.probability)
            self.weak = 1

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)
            listener = Listener(Listener.Event.START_TURN, weak.decrement)
            player.add_listener(listener)

    class Tackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 10
            else:
                self.damage = 12

            self.probability = 40

            super().__init__("Tackle", self.damage, 1, 0, self.probability)

    class CorrosiveSpit(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 7
            else:
                self.damage = 8

            if ascension < 17:
                self.probability = 30
            else:
                self.probability = 40
            self.num_cards = 1
            super().__init__("Corrosive Spit", self.damage, 1, 0, self.probability)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.append(Slimed(player))
