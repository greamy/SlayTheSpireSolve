from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class SingingBowl(Relic):
    # When adding cards to your deck, you may gain +2 Max HP instead.

    def __init__(self, player):
        super().__init__("Singing Bowl", "Uncommon", player)
        # TODO: implement the effect of this relic on the player here probably.

    def on_pickup(self):
        pass

    def on_drop(self):
        pass
