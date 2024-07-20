from Entities.Player import Player
from Actions.Card import Card


class Collect(Card):
    def __init__(self):
        super().__init__("Collect", 0, 0, 0, 0, 0, 0, True, "", None)