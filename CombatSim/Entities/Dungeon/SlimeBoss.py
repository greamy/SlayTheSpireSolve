from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Slimed import Slimed
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Dungeon.AcidSlimeLarge import AcidSlimeLarge
from CombatSim.Entities.Dungeon.SpikedSlimeLarge import SpikedSlimeLarge
from CombatSim.Entities.Enemy import Enemy
import random
from CombatSim.Entities.Player import Player


class SlimeBoss(Enemy):
    GOOPSPRAY = 0
    PREPARE = 1
    SLAM = 2
    SPLIT = 3

    def __init__(self, ascension: int, act: int, ):

        intent_set = [self.GoopSpray(ascension),
                      self.Prepare(ascension),
                      self.Slam(ascension),
                      self.Split(ascension, act)
                      ]
        self.pattern_index = 1
        self.split = False

        if ascension < 9:
            super().__init__(140, intent_set, ascension, minion=False)
        else:
            super().__init__(150, intent_set, ascension, minion=False)
        self.start_health = self.health
        self.pattern = [self.intent_set[self.GOOPSPRAY], self.intent_set[self.PREPARE],
                        self.intent_set[self.SLAM]]

    def choose_intent(self):
        if self.num_turns == 0:
            self.intent = self.intent_set[self.GOOPSPRAY]
        else:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health <= self.start_health and not self.split:
            self.intent = self.intent_set[self.SPLIT]
            self.split = True

    class GoopSpray(Intent):
        def __init__(self, ascension: int):

            if ascension < 19:
                self.slimed = 3
            else:
                self.slimed = 5
            super().__init__("GoopSpray", 0, 0, 0, 0)

        def play(self, enemy, enemy_list, player, player_list, debug):
            for _ in range(self.slimed):
                player.deck.discard_pile.append(Slimed(player))

    class Prepare(Intent):
        def __init__(self, ascension):
            super().__init__("Prepare", 0, 0, 0, 1)

    class Slam(Intent):
        def __init__(self, ascension: int):
            if ascension < 4:
                self.damage = 35
            else:
                self.damage = 38

            super().__init__("Slam", self.damage, 1, 0, 2)

    class Split(Intent):
        def __init__(self, ascension: int, act: int):
            self.ascension = ascension
            self.act = act
            super().__init__("Split", 0, 0, 0, 97)

        def play(self, enemy: Enemy, enemy_list: list[Enemy], player: Player, player_list: list[Player], debug: bool):
            slime1 = SpikedSlimeLarge(self.ascension, self.act)
            slime2 = AcidSlimeLarge(self.ascension, self.act)
            slime1.health = enemy.health
            slime2.health = enemy.health
            enemy_list.extend([slime1, slime2])
            enemy_list.remove(enemy)
