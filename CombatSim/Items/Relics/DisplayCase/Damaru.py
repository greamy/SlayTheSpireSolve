from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Damaru(Relic):
    # If you do not play any Attacks during your turn, gain an extra Energy next turn.
    def __init__(self, player):
        super().__init__("Damaru", "Common", player)
        self.start_turn_listener = Listener(Listener.Event.START_TURN, self.on_start_turn)

    def on_start_turn(self, player, enemy, enemies, debug):
        player.add_mantra(1)

    def on_pickup(self):
        self.player.add_listener(self.start_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.start_turn_listener)

