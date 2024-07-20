from Entities.Player import Player
from Actions.Card import Card


class Devotion(Card):
    def __init__(self):
        super().__init__("Devotion", 1, 0, 0, 0, 0, 0, False, "", None)