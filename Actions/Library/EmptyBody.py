from Entities.Player import Player
from Actions.Card import Card


class EmptyBody(Card):
    def __init__(self):
        super().__init__("EmptyBody", 1, 0, 0, 7, 0, 0, False, "", Player.Stance.NONE)