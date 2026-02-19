from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Shuriken(Relic):
    # Every time you play 3 Attacks in a single turn, gain 1 Dexterity.
    def __init__(self, player):
        super().__init__("Shuriken", "Common", player)
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.on_attack_played)
        self.end_turn_listener = Listener(Listener.Event.END_TURN, self.on_end_turn)
        self.attack_count = 0

    def on_attack_played(self, player, enemy, enemies, debug):
        self.attack_count += 1
        if self.attack_count == 3:
            player.damage_dealt_modifier += 1
            self.attack_count = 0

    def on_end_turn(self, player, enemy, enemies, debug):
        self.attack_count = 0

    def on_pickup(self):
        self.player.add_listener(self.attack_listener)
        self.player.add_listener(self.end_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.attack_listener)
        self.player.remove_listener(self.end_turn_listener)

