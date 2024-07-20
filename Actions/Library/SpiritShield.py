from Entities.Player import Player
from Actions.Card import Card


class SpiritShield(Card):
    def __init__(self):
        super().__init__("SpiritShield", 2, 0, 0, 3, 0, 0, False, "", None)