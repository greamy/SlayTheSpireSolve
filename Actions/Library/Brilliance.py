from Entities.Player import Player
from Actions.Card import Card


class Brilliance(Card):
    def __init__(self):
        super().__init__("Brilliance", 1, 12, 1, 0, 0, 0, False, "", None)