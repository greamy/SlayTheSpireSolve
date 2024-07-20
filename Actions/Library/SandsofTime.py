from Entities.Player import Player
from Actions.Card import Card


class SandsofTime(Card):
    def __init__(self):
        super().__init__("SandsofTime", 4, 20, 1, 0, 0, 0, False, "", None)