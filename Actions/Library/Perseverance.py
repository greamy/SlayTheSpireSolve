from Entities.Player import Player
from Actions.Card import Card


class Perseverance(Card):
    def __init__(self):
        super().__init__("Perseverance", 1, 0, 0, 5, 0, 0, False, "", None)