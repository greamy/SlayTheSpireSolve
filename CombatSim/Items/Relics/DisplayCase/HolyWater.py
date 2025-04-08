from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic
from CombatSim.Actions.Library.Miracle import Miracle


class HolyWater(Relic):
    # Adds Miracle to hand at start of combat
    def __init__(self, player):
        super().__init__("Holy Water", "Starter", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.add_miracle)

    def add_miracle(self, player, enemy, enemies, debug):
        self.player.deck.hand.append(Miracle(player))
    
    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)
