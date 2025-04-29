from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic


class TheBoot(Relic):
    def __init__(self, player):
        super().__init__("The Boot", "Common", player)