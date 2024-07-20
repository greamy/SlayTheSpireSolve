from Entities.Player import Player
from Actions.Card import Card


class Meditate(Card):
    def __init__(self):
        super().__init__("Meditate", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.CALM)