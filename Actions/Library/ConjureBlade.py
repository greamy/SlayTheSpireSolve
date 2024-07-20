from Entities.Player import Player
from Actions.Card import Card


class ConjureBlade(Card):
    def __init__(self):
        super().__init__("ConjureBlade", 0, 0, 0, 0, 0, 0, True, "", None)