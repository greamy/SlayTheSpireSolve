from CombatSim.Items.Relics.Relic import Relic

class ArtOfWar(Relic):
    # If you do not play any Attacks during your turn, gain an extra Energy next turn.
    def __init__(self, player):
        super().__init__("Art of War", "Common", player)
