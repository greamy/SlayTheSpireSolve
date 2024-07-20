from Entities.Player import Player
from Actions.Card import Card


class Consecrate(Card):
    def __init__(self):
        super().__init__("Consecrate", 0, 5, 1, 0, 0, 0, False, "", None)