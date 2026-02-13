from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

class Lantern(Relic):
    # Gain 1 Energy on the first turn of each combat.
    def __init__(self, player):
        super().__init__("Lantern", "Common", player)

        self.listener = Listener(Listener.Event.START_COMBAT, self.on_start_combat)
        self.start_turn_listener = Listener(Listener.Event.START_TURN, self.on_start_turn)
        self.start_flag = False

    def on_start_combat(self, player, enemy, enemies, debug):
        self.start_flag = True

    def on_start_turn(self, player, enemy, enemies, debug):
        if self.start_flag:
            player.energy += 1
            self.start_flag = False

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.start_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.start_turn_listener)
