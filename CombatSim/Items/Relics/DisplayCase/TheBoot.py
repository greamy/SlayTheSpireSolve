from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic

import numpy as np


class TheBoot(Relic):
    # Whenever you would deal 4 or less unblocked Attack damage, increase it to 5.
    def __init__(self, player):
        super().__init__("The Boot", "Common", player)
        self.listener = Listener(Listener.Event.TAKEN_DAMAGE, self.modify_damage)
        self.start_combat_listen = Listener(Listener.Event.START_COMBAT, self.add_self_to_enemies)
        self.update_healths = Listener(Listener.Event.START_TURN, self.update_enemy_healths)
        self.enemy_hp_pools = np.array([])


    def modify_damage(self, player, enemy, enemies, debug):
        new_hp_pools = [en.health for en in enemies]
        index = np.nonzero(self.enemy_hp_pools - new_hp_pools)[0]
        if len(index) == 0:
            return
        else:
            index = int(index[0])
        if self.enemy_hp_pools[index] - enemy.health <= 4:
            enemy.health -= 5 - (self.enemy_hp_pools[index] - enemy.health)

        self.enemy_hp_pools[index] = enemy.health

    def update_enemy_healths(self, player, enemy, enemies, debug):
        for i, enemy in enumerate(enemies):
            self.enemy_hp_pools[i] = enemy.health

    def add_self_to_enemies(self, player, enemy, enemies, debug):
        for enemy in enemies:
            enemy.add_listener(self.listener)
            self.enemy_hp_pools = np.append(self.enemy_hp_pools, enemy.health)

    def on_pickup(self):
        self.player.add_listener(self.start_combat_listen)
        self.player.add_listener(self.update_healths)

    def on_drop(self):
        self.player.listeners.remove(self.listener)