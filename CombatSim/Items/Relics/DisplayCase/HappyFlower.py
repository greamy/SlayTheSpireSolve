from CombatSim.Items.Relics.Relic import Relic

class HappyFlower(Relic):
    # Every 3 turns, gain 1 Energy.
    def __init__(self, player):
        super().__init__("Happy Flower", "Common", player)
