from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class HappyFlower(Relic):
    # Every 3 turns, gain 1 Energy.
    def __init__(self, player):
        super().__init__("Happy Flower", "Common", player)
        self.start_turn_listener = Listener(Listener.Event.START_TURN, self.start_turn)
        self.turn_ct = 0

    def start_turn(self, player, enemy, enemies, debug):
        self.turn_ct += 1
        if self.turn_ct >= 3:
            self.player.energy += 1
            self.turn_ct = 0

    def on_pickup(self):
        self.player.add_listener(self.start_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.start_turn_listener)