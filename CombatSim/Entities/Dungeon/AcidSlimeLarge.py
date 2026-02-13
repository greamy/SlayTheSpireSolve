import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Slimed import Slimed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Dungeon.AcidSlimeMedium import AcidSlimeMedium
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Status.Weak import Weak


class AcidSlimeLarge(Enemy):
    SPLIT = 0
    LICK = 1
    TACKLE = 2
    CORROSIVE_SPIT = 3

    def __init__(self, ascension: int, act: int):
        intent_set = [
            self.Split(ascension, act),
            self.Lick(ascension),
            self.Tackle(ascension),
            self.CorrosiveSpit(ascension)
        ]
        self.ascension = ascension
        if ascension < 7:
            super().__init__(random.randint(65, 69), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(68, 72), intent_set, ascension, minion=False)

        self.start_health = self.health

        self.split = False

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        if self.ascension < 17:
            if intent == self.intent_set[self.TACKLE] and self.num_consecutive == 2:
                return False
            if (intent == self.intent_set[self.CORROSIVE_SPIT] or intent == self.intent_set[self.LICK]) and self.num_consecutive == 3:
                return False
        else:
            if intent == self.intent_set[self.LICK] and self.num_consecutive == 2:
                return False
            if (intent == self.intent_set[self.CORROSIVE_SPIT] or intent == self.intent_set[self.TACKLE]) and self.num_consecutive == 3:
                return False

        return True

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health <= self.start_health and not self.split:
            self.intent = self.intent_set[self.SPLIT]
            self.split = True

    class Lick(Intent):
        def __init__(self, ascension: int):
            self.probability = 30
            super().__init__("Lick", 0, 0, 0, self.probability, char.Intent.DEBUFF)
            self.weak = 2

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            weak = Weak(self.weak, player)

    class Tackle(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 16
            else:
                self.damage = 18

            if ascension < 17:
                self.probability = 40
            else:
                self.probability = 30

            super().__init__("Tackle", self.damage, 1, 0, self.probability, char.Intent.ATTACK)

    class CorrosiveSpit(Intent):
        def __init__(self, ascension):
            if ascension < 2:
                self.damage = 11
            else:
                self.damage = 12

            if ascension < 17:
                self.probability = 30
            else:
                self.probability = 40
            self.num_cards = 2
            super().__init__("Corrosive Spit", self.damage, 1, 0, self.probability, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            super().play(enemy, enemy_list, player, player_list, debug)
            player.deck.discard_pile.extend([Slimed(player) for _ in range(self.num_cards)])

    class Split(Intent):
        def __init__(self, ascension, act):
            self.act = act
            self.ascension = ascension
            super().__init__("Split", 0, 0, 0, 0, char.Intent.UNKNOWN)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            slime1 = AcidSlimeMedium(self.ascension, self.act)
            slime2 = AcidSlimeMedium(self.ascension, self.act)
            slime1.health = enemy.health
            slime2.health = enemy.health
            enemy_list.extend([slime1, slime2])
            enemy_list.remove(enemy)
