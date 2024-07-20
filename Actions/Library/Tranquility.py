from Entities.Player import Player
from Actions.Card import Card


class Tranquility(Card):
    def __init__(self):
        super().__init__("Tranquility", 1, 0, 0, 0, 0, 0, True, "", Player.Stance.CALM)