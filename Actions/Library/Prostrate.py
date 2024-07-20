from Entities.Player import Player
from Actions.Card import Card


class Prostrate(Card):
    def __init__(self):
        super().__init__("Prostrate", 0, 0, 0, 0, 0, 0, False, "", None)