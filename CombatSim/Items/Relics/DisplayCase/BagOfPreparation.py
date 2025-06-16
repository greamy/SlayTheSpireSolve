from CombatSim.Items.Relics.Relic import Relic

class BagOfPreparation(Relic):
    # At the start of each combat, draw 2 additional cards.
    def __init__(self, player):
        super().__init__("Bag Of Preparation", "Common", player)
