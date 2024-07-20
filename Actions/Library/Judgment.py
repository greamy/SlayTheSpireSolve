from Entities.Player import Player
from Actions.Card import Card


class Judgment(Card):
    def __init__(self):
        super().__init__("Judgment", 1, 0, 0, 0, 0, 0, False, "", None)