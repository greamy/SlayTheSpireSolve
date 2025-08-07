from CombatSim.Actions.Library.Miracle import Miracle
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic


class PureWater(Relic):
    # Your first attack each combat deals 8  additional damage.
    def __init__(self, player):
        super().__init__("Pure Water", "common", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.add_card)

    def add_card(self, player, enemy, enemies, debug):
        self.player.deck.hand.append(Miracle(player))

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)