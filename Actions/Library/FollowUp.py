from Entities.Player import Player
from Actions.Card import Card


class FollowUp(Card):
    def __init__(self):
        super().__init__("FollowUp", 1, 7, 1, 0, 0, 0, False, "", None)