from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic


class SsserpentHead(Relic):
    # Whenever you enter a ? room, gain 50 Gold.
    GOLD = 50

    def __init__(self, player):
        super().__init__("SsserpentHead", "Event", player)
        self.listener = Listener(Listener.Event.ENTER_EVENT, self.gain_gold)

    def gain_gold(self, player, enemy, enemies, debug):
        self.player.gold += self.GOLD

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)