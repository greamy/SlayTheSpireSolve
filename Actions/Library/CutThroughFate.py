from Entities.Player import Player
from Actions.Card import Card


class CutThroughFate(Card):
    def __init__(self):
        super().__init__("CutThroughFate", 1, 7, 1, 0, 0, 0, False, "", None)