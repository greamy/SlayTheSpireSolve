from Entities.Player import Player
from Actions.Card import Card


class FearNoEvil(Card):
    def __init__(self):
        super().__init__("FearNoEvil", 1, 8, 1, 0, 0, 0, False, "", None)