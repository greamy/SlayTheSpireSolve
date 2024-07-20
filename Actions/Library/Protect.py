from Entities.Player import Player
from Actions.Card import Card


class Protect(Card):
    def __init__(self):
        super().__init__("Protect", 2, 0, 0, 12, 0, 0, False, "", None)