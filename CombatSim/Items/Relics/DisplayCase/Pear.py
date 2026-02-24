from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Pear(Relic):
    # Upon pickup, raise your Max HP by 10.
    MAX_HP_AMOUNT = 10

    def __init__(self, player):
        super().__init__("Pear", "Uncommon", player)

    def on_pickup(self):
        self.player.add_max_hp(self.MAX_HP_AMOUNT)

    def on_drop(self):
        pass
