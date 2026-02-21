from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class WhiteBestStatue(Relic):
    # Potions always drop after combat.

    def __init__(self, player):
        super().__init__("White Beast Statue", "Uncommon", player)
        # TODO: implement the effect of this relic on the player here probably.

    def on_pickup(self):
        pass

    def on_drop(self):
        pass
