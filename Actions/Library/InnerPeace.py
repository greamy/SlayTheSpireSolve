from Entities.Player import Player
from Actions.Card import Card


class InnerPeace(Card):
    def __init__(self):
        super().__init__("InnerPeace", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.CALM)