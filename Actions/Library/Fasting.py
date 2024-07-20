from Entities.Player import Player
from Actions.Card import Card


class Fasting(Card):
    def __init__(self):
        super().__init__("Fasting", 2, 0, 0, 0, 0, 0, False, "", None)