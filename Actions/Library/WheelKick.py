from Entities.Player import Player
from Actions.Card import Card


class WheelKick(Card):
    def __init__(self):
        super().__init__("WheelKick", 2, 15, 1, 0, 0, 0, False, "", None)