from CombatSim.Items.Relics.Relic import Relic

class CentennialPuzzle(Relic):
    # The first time you lose HP each combat, draw 3 cards.
    def __init__(self, player):
        super().__init__("Centennial Puzzle", "Common", player)
