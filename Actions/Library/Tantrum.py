from Entities.Player import Player
from Actions.Card import Card


class Tantrum(Card):
    def __init__(self):
        super().__init__("Tantrum", 1, 3, 3, 0, 0, 0, False, "", Player.Stance.WRATH)