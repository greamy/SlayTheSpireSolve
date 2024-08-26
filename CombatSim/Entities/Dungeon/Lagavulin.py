from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
import random

from CombatSim.Entities.Metallicize import Metallicize
from CombatSim.Entities.Player import Player

class Lagavulin(Enemy):
    ATTACK = 0
    SIPHONSOUL = 1
    SLEEP = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Sleep(ascension),
                      self.Attack(ascension),
                      self.SiphonSoul(ascension),
                      ]

        self.sleep = True

        if ascension < 8:
            super().__init__(random.randint(109, 111), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(112, 115), intent_set, ascension, minion=False)

        self.start_health = self.health
        self.pattern_index = 0
        self.pattern = [self.intent_set[self.ATTACK], self.intent_set[self.ATTACK],
                        self.intent_set[self.SIPHONSOUL]]

        self.metallicize_amount = 8
        self.metallicize = Metallicize(self.metallicize_amount, self)

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health < self.start_health :
            self.sleep = False
            self.metallicize.remove()

    def choose_intent(self):
        if self.num_turns < 3 and self.sleep:
            self.intent = self.intent_set[self.SLEEP]
        else:
            if self.pattern_index >= len(self.pattern):
                self.pattern_index = 0
            self.intent = self.pattern[self.pattern_index]
            self.pattern_index += 1

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Sleep(Intent):
        def __init__(self, ascension: int):
            super().__init__("Sleep", 0, 0, 0, 100)

        def play(self, enemy, enemy_list, player, player_list, debug):
            pass


    class Attack(Intent):
        def __init__(self, ascension: int):
            if ascension < 3:
                self.damage = 18
            else:
                self.damage = 20
            super().__init__("Attack", self.damage, 1, 0, 0)

    class SiphonSoul(Intent):
        def __init__(self, ascension: int):
            if ascension < 18:
                self.debuf = 1
            else:
                self.debuf = 2
            super().__init__("SiphonSoul", 0, 0, 0, 0)

        def play(self, enemy, enemy_list, player, player_list, debug):
            player.block_modifier -= self.debuf
            player.damage_dealt_modifier -= self.debuf


