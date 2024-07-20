from Entities.Player import Player
from Actions.Card import Card


class Alpha(Card):
    def __init__(self):
        super().__init__("Alpha", 1, 0, 0, 0, 0, 0, True, "", None)