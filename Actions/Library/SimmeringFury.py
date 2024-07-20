from Entities.Player import Player
from Actions.Card import Card


class SimmeringFury(Card):
    def __init__(self):
        super().__init__("SimmeringFury", 1, 0, 0, 0, 0, 0, False, "", None)