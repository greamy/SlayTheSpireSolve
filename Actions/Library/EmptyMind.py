from Entities.Player import Player
from Actions.Card import Card


class EmptyMind(Card):
    def __init__(self):
        super().__init__("EmptyMind", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.NONE)