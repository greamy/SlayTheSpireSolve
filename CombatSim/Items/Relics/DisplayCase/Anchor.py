from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic



class Anchor(Relic):
    # Adds 10 block on turn one
    def __init__(self, player):
        super().__init__("Anchor", "Common", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.add_start_block)

    def add_start_block(self, player, enemy, enemies, debug):
        self.player.block += 10

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)
