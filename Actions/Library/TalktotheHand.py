from Entities.Player import Player
from Actions.Card import Card


class TalktotheHand(Card):
    def __init__(self):
        super().__init__("TalktotheHand", 1, 5, 1, 0, 0, 0, True, "", None)