from Entities.Player import Player
from Actions.Card import Card


class SignatureMove(Card):
    def __init__(self):
        super().__init__("SignatureMove", 2, 30, 1, 0, 0, 0, False, "", None)