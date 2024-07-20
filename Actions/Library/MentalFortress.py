from Entities.Player import Player
from Actions.Card import Card


class MentalFortress(Card):
    def __init__(self):
        super().__init__("MentalFortress", 1, 0, 0, 0, 0, 0, False, "", None)