from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Strawberry(Relic):
    # The merchant's card removal service now always costs 50 Gold.
    MAX_HP_AMOUNT = 6

    def __init__(self, player):
        super().__init__("Strawberry", "Common", player)

    def on_pickup(self):
        self.player.add_max_hp(self.MAX_HP_AMOUNT)

    def on_drop(self):
        pass
