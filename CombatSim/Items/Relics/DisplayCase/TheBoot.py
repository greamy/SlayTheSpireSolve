from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic

import numpy as np


class TheBoot(Relic):
    BOOT_DAMAGE = 5
    # Whenever you would deal 4 or less unblocked Attack damage, increase it to 5.
    def __init__(self, player):
        super().__init__("The Boot", "Common", player)
        self.listener = Listener(Listener.Event.TAKEN_DAMAGE, self.modify_damage)
        self.start_combat_listen = Listener(Listener.Event.START_COMBAT, self.add_self_to_enemies)
        self.update_healths = Listener(Listener.Event.START_TURN, self.update_enemy_healths)
        self.enemy_hps: {Enemy: int} = {}


    def modify_damage(self, enemy, player, players, debug):
        if self.enemy_hps[enemy] - enemy.health <= (self.BOOT_DAMAGE-1):
            enemy.health -= self.BOOT_DAMAGE - (self.enemy_hps[enemy] - enemy.health)

        self.enemy_hps[enemy] = enemy.health

    def update_enemy_healths(self, player, enemy, enemies, debug):
        for i, enemy in enumerate(enemies):
            self.enemy_hps[enemy] = enemy.health

    def add_self_to_enemies(self, player, enemy, enemies, debug):
        for enemy in enemies:
            enemy.add_listener(self.listener)
            self.enemy_hps[enemy] = enemy.health

    def on_pickup(self):
        self.player.add_listener(self.start_combat_listen)
        self.player.add_listener(self.update_healths)

    def on_drop(self):
        self.player.listeners.remove(self.listener)