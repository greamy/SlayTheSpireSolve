from Entities.Player import Player
from Actions.Card import Card


class Ragnarok(Card):
    def __init__(self):
        super().__init__("Ragnarok", 3, 5, 1, 0, 0, 0, False, "", None)