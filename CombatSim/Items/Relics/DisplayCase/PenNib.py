from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class PenNib(Relic):
    # Every 10th Attack you play deals double damage.
    def __init__(self, player):
        super().__init__("PenNib", "Common", player)
        self.player = player
        self.enemy_hps = {}
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.attack_was_played)
        self.start_combat_listener = Listener(Listener.Event.START_COMBAT, self.on_start_combat)
        self.current_attack_count = 0

    def attack_was_played(self, player, enemy, enemies, debug):
        self.current_attack_count += 1
        if self.current_attack_count == 10:
            health_lost = self.enemy_hps[enemy] - enemy.health + enemy.block
            enemy.take_damage(health_lost)
            self.current_attack_count = 0

        self.enemy_hps = {}
        for enemy in enemies:
            self.enemy_hps[enemy] = enemy.health

    def on_start_combat(self, player, enemy, enemies, debug):
        self.enemy_hps = {}
        for enemy in enemies:
            self.enemy_hps[enemy] = enemy.health + enemy.block

    def on_pickup(self):
        self.player.add_listener(self.attack_listener)

    def on_drop(self):
        self.player.remove_listener(self.attack_listener)

