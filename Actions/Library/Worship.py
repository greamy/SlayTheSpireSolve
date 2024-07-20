from Entities.Player import Player
from Actions.Card import Card


class Worship(Card):
    def __init__(self):
        super().__init__("Worship", 2, 0, 0, 0, 0, 0, False, "", None)