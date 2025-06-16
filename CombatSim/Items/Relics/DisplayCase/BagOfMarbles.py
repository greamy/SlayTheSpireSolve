from CombatSim.Items.Relics.Relic import Relic

class BagOfMarbles(Relic):
    # At the start of each combat, apply 1  Vulnerable to ALL enemies.
    def __init__(self, player):
        super().__init__("Bag Of Marbles", "Common", player)
