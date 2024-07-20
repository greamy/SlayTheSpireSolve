from Entities.Player import Player
from Actions.Card import Card


class Weave(Card):
    def __init__(self):
        super().__init__("Weave", 0, 4, 1, 0, 0, 0, False, "", None)