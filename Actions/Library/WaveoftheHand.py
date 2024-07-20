from Entities.Player import Player
from Actions.Card import Card


class WaveoftheHand(Card):
    def __init__(self):
        super().__init__("WaveoftheHand", 1, 0, 0, 0, 0, 0, False, "", None)