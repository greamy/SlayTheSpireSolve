from Entities.Player import Player
from Actions.Card import Card


class Vigilance(Card):
    def __init__(self):
        super().__init__("Vigilance", 2, 0, 0, 8, 0, 0, False, "", Player.Stance.CALM)