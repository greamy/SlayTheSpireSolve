
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class HornCleat(Relic):
    # At the start of your 2nd turn, gain 14 Block.
    BLOCK_GAIN = 14
    TURN_NUMBER = 2

    def __init__(self, player):
        super().__init__("Horn Cleat", "Common", player)
        self.listener = Listener(Listener.Event.START_TURN, self.on_start_turn)
        self.end_combat_reset_listener = Listener(Listener.Event.END_COMBAT, self.on_end_combat)
        self.turn_count = 0

    def on_start_turn(self, player, enemy, enemies, debug):
        self.turn_count += 1
        if self.turn_count == self.TURN_NUMBER:
            self.player.gain_block(self.BLOCK_GAIN, enemies, debug)

    def on_end_combat(self, player, enemy, enemies, debug):
        self.turn_count = 0

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.end_combat_reset_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.end_combat_reset_listener)
