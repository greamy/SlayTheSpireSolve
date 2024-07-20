from Entities.Player import Player
from Actions.Card import Card


class Blasphemy(Card):
    def __init__(self):
        super().__init__("Blasphemy", 1, 0, 0, 0, 0, 0, True, "", Player.Stance.DIVINITY)