from Entities.Player import Player
from Actions.Card import Card


class BowlingBash(Card):
    def __init__(self):
        super().__init__("BowlingBash", 1, 7, 1, 0, 0, 0, False, "", None)