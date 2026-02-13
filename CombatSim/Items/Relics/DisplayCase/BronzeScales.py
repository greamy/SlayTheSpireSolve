
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Thorns import Thorns
from CombatSim.Items.Relics.Relic import Relic

class BronzeScales(Relic):
    # At the start of each combat, gain 3 thorns.
    THORNS_AMOUNT = 3
    def __init__(self, player):
        super().__init__("Bronze Scales", "Common", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.start_combat)

    def start_combat(self, player, enemy, enemies, debug):
        thorns = Thorns(self.THORNS_AMOUNT, player)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)