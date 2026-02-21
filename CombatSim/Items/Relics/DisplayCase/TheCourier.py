from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class TheCourier(Relic):
    # The merchant no longer runs out of cards, relics, or potions and his prices are reduced by 20%.

    def __init__(self, player):
        super().__init__("The Courier", "Uncommon", player)
        # TODO: implement the effect of this relic on the player here probably.

    def on_pickup(self):
        pass

    def on_drop(self):
        pass
