from Entities.Player import Player
from Actions.Card import Card


class PressurePoints(Card):
    def __init__(self):
        super().__init__("PressurePoints", 1, 0, 0, 0, 0, 0, False, "", None)