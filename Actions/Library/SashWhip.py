from Entities.Player import Player
from Actions.Card import Card


class SashWhip(Card):
    def __init__(self):
        super().__init__("SashWhip", 1, 8, 1, 0, 0, 0, False, "", None)