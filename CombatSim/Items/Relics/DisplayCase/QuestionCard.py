from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class QuestionCard(Relic):
    # On future Card Reward screens you have 1 additional card to choose from.

    def __init__(self, player):
        super().__init__("Question Card", "Uncommon", player)
        # TODO: implement the effect of this relic on the player here probably.

    def on_pickup(self):
        pass

    def on_drop(self):
        pass
