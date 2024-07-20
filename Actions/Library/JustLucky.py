from Entities.Player import Player
from Actions.Card import Card


class JustLucky(Card):
    def __init__(self):
        super().__init__("JustLucky", 0, 3, 1, 2, 0, 0, False, "", None)