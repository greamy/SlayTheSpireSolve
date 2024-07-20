from Entities.Player import Player
from Actions.Card import Card


class Foresight(Card):
    def __init__(self):
        super().__init__("Foresight", 1, 0, 0, 0, 0, 0, False, "", None)