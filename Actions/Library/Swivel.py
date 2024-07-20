from Entities.Player import Player
from Actions.Card import Card


class Swivel(Card):
    def __init__(self):
        super().__init__("Swivel", 2, 0, 0, 8, 0, 0, False, "", None)