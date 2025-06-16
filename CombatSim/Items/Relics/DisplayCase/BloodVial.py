from CombatSim.Items.Relics.Relic import Relic

class BloodVial(Relic):
    # At the start of each combat, heal 2 HP.
    def __init__(self, player):
        super().__init__("Blood Vial", "Common", player)
