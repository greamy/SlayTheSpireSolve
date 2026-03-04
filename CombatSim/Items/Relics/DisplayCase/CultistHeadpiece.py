from CombatSim.Items.Relics.Relic import Relic


class CultistHeadpiece(Relic):
    # You feel more talkative. No mechanical effect.
    def __init__(self, player):
        super().__init__("CultistHeadpiece", "Event", player)