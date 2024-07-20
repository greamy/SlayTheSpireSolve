from Entities.Player import Player
from Actions.Card import Card


class Omniscience(Card):
    def __init__(self):
        super().__init__("Omniscience", 4, 0, 0, 0, 0, 0, False, "", None)