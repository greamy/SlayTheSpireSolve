from Entities.Player import Player
from Actions.Card import Card


class CarveReality(Card):
    def __init__(self):
        super().__init__("CarveReality", 1, 6, 1, 0, 0, 0, False, "", None)