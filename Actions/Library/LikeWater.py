from Entities.Player import Player
from Actions.Card import Card


class LikeWater(Card):
    def __init__(self):
        super().__init__("LikeWater", 1, 0, 0, 0, 0, 0, False, "", None)