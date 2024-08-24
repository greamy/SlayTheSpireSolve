from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Slimed import Slimed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Dungeon.SpikedSlimeMedium import SpikedSlimeMedium
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Frail import Frail
from CombatSim.Entities.Player import Player


class SpikedSlimeLarge(Enemy):
    # Must be ordered based on probability. Lowest to highest.
    SPLIT = 0
    FLAMETACKLE = 1
    LICK = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Split(ascension, act), self.FlameTackle(ascension), self.Lick(ascension)]
        if ascension < 7:
            super().__init__(random.randint(64, 70), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(67, 73), intent_set, ascension, minion=False)

        if ascension < 17:
            self.lick_consec = 2
        else:
            self.lick_consec = 3

        self.split = False
        self.start_health = self.health

    def choose_intent(self):
        if self.intent == self.intent_set[self.FLAMETACKLE] and self.num_consecutive == 3:
            self.intent = self.intent_set[self.LICK]
        elif self.intent == self.intent_set[self.LICK] and self.num_consecutive == self.lick_consec:
            self.intent = self.intent_set[self.FLAMETACKLE]
        else:
            super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health <= self.start_health and not self.split:
            self.intent = self.intent_set[self.SPLIT]
            self.split = True

    class FlameTackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 16
            else:
                self.damage = 18
            super().__init__("Tackle", self.damage, 1, 0, 30)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.append(Slimed(player))
            player.deck.discard_pile.append(Slimed(player))

    class Lick(Intent):
        def __init__(self, ascension: int):
            if ascension < 17:
                self.frail = 2
            else:
                self.frail = 3
            super().__init__("Lick", 0, 0, 0, 70)

        def play(self, enemy, enemy_list, player, player_list, debug):
            super().play(enemy, enemy_list, player, player_list, debug)
            frail = Frail(self.frail, player)
            listener = Listener(Listener.Event.START_TURN, frail.decrement)
            player.add_listener(listener)

    class Split(Intent):
        def __init__(self, ascension: int, act):
            self.act = act
            self.ascension = ascension
            super().__init__("Split", 0, 0, 0, 0)

        def play(self, enemy, enemy_list, player, player_list, debug):
            slime1 = SpikedSlimeMedium(self.ascension, self.act)
            slime2 = SpikedSlimeMedium(self.ascension, self.act)
            slime1.health = enemy.health
            slime2.health = enemy.health
            enemy_list.extend([slime1, slime2])
            enemy_list.remove(enemy)
