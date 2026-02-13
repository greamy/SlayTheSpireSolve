from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic

class Orichalcum(Relic):
    # If you end your turn without Icon Block Block, gain 6 Icon Block Block.
    def __init__(self, player):
        super().__init__("Orichalcum", "common", player)
        self.listener = Listener(Listener.Event.END_TURN, self.block_check)

    def block_check(self, player, enemy, enemies, debug):
        if self.player.block == 0:
            self.player.block += 6

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)
