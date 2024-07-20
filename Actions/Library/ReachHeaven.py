from Entities.Player import Player
from Actions.Card import Card


class ReachHeaven(Card):
    def __init__(self):
        super().__init__("ReachHeaven", 2, 10, 1, 0, 0, 0, False, "", None)