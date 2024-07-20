from Entities.Player import Player
from Actions.Card import Card


class Indignation(Card):
    def __init__(self):
        super().__init__("Indignation", 1, 0, 0, 0, 0, 0, False, "", None)