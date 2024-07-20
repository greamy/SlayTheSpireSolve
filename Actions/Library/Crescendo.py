from Entities.Player import Player
from Actions.Card import Card


class Crescendo(Card):
    def __init__(self):
        super().__init__("Crescendo", 1, 0, 0, 0, 0, 0, True, "", Player.Stance.WRATH)