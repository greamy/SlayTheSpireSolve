from Entities.Player import Player
from Actions.Card import Card


class Strike(Card):
    def __init__(self):
        super().__init__("Strike", 1, 6, 1, 0, 0, 0, False, "", None)