from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Nunchaku(Relic):
    # Every time you play 10 Attacks, gain 1 Energy.
    def __init__(self, player):
        super().__init__("Nunchaku", "Common", player)
        self.player = player
        self.attack_played = False
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.attack_was_played)
        self.current_attack_count = 0

    def attack_was_played(self, player, enemy, enemies, debug):
        self.current_attack_count += 1
        if self.current_attack_count == 10:
            player.energy += 1
            self.current_attack_count = 0

    def on_pickup(self):
        self.player.add_listener(self.attack_listener)

    def on_drop(self):
        self.player.remove_listener(self.attack_listener)

