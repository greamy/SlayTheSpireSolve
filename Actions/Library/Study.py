from Entities.Player import Player
from Actions.Card import Card


class Study(Card):
    def __init__(self):
        super().__init__("Study", 2, 0, 0, 0, 0, 0, False, "", None)