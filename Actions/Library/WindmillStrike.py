from Entities.Player import Player
from Actions.Card import Card


class WindmillStrike(Card):
    def __init__(self):
        super().__init__("WindmillStrike", 2, 7, 1, 0, 0, 0, False, "", None)