from Entities.Player import Player
from Actions.Card import Card


class Sanctity(Card):
    def __init__(self):
        super().__init__("Sanctity", 1, 0, 0, 6, 0, 0, False, "", None)