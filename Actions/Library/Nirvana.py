from Entities.Player import Player
from Actions.Card import Card


class Nirvana(Card):
    def __init__(self):
        super().__init__("Nirvana", 1, 0, 0, 0, 0, 0, False, "", None)