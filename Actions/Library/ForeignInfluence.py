from Entities.Player import Player
from Actions.Card import Card


class ForeignInfluence(Card):
    def __init__(self):
        super().__init__("ForeignInfluence", 0, 0, 0, 0, 0, 0, True, "", None)