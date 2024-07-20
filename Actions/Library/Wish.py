from Entities.Player import Player
from Actions.Card import Card


class Wish(Card):
    def __init__(self):
        super().__init__("Wish", 3, 0, 0, 0, 0, 0, True, "", None)