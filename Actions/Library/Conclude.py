from Entities.Player import Player
from Actions.Card import Card


class Conclude(Card):
    def __init__(self):
        super().__init__("Conclude", 1, 12, 1, 0, 0, 0, False, "", None)