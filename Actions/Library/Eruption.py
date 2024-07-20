from Entities.Player import Player
from Actions.Card import Card


class Eruption(Card):
    def __init__(self):
        super().__init__("Eruption", 2, 9, 1, 0, 0, 0, False, "", Player.Stance.WRATH)