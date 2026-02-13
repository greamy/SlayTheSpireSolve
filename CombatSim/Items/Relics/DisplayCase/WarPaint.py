from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

import numpy as np

class WarPaint(Relic):
    # Upon pick up, Upgrade 2 random Skills.
    def __init__(self, player):
        super().__init__("War Paint", "Common", player)

    def on_pickup(self):
        un_upgraded_skills = []
        for card in self.player.deck:
            if not card.upgraded and card.card_type == card.Type.SKILL:
                un_upgraded_skills.append(card)

        choices = np.random.choice(un_upgraded_skills, 2 if len(un_upgraded_skills) >= 2 else len(un_upgraded_skills), replace=False)
        for card in choices:
            card.upgrade()

    def on_drop(self):
        pass
