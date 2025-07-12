import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Frail import Frail
from CombatSim.Actions.Listener import Listener

class Mystic(Enemy):
    HEAL = 2
    ATTACKDEBUFF = 0
    BUFF = 1

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Heal(ascension), self.Attack_Debuff(ascension), self.Buff(ascension)]

        if ascension < 7:
            super().__init__(random.randint(48, 56), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(50, 58), intent_set, ascension, minion=False)

    def choose_intent(self):
        super().choose_intent()

    def is_valid_intent(self, intent: Intent) -> bool:
        return True

    class Heal(Intent):
        def __init__(self, ascension: int):
            if ascension < 17:
                self.heal = 16
            else:
                self.heal = 20
            super().__init__("Heal", 0, 0, 0, 0, char.Intent.BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            for enemy in enemy_list:
                enemy.health += self.heal
            super().play(enemy, enemy_list, player, player_list, debug)

    class Buff(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.strength = 2
            elif ascension < 17:
                self.strength = 3
            else:
                self.strength = 4
            super().__init__("Buff", 0, 0, 0, 40, char.Intent.ATTACK_BUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            for enemy in enemy_list:
                enemy.damage_dealt_modifier += self.strength
            super().play(enemy, enemy_list, player, player_list, debug)

    class Attack_Debuff(Intent):
        def __init__(self, ascension: int):
            self.frail = 2
            if ascension < 2:
                self.damage = 8
            else:
                self.damage = 9
            super().__init__("Attack/Debuff", self.damage, 0, 0, 60, char.Intent.ATTACK_DEBUFF)

        def play(self, enemy, enemy_list, player, player_list, debug):
            frail = Frail(self.frail, player)
            player.add_listener(Listener(Listener.Event.START_TURN, frail.decrement))
            super().play(enemy, enemy_list, player, player_list, debug)
