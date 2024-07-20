from Entities.Player import Player
from Actions.Card import Card


class WreathofFlame(Card):
    def __init__(self):
        super().__init__("WreathofFlame", 1, 0, 0, 0, 0, 0, False, "", None)