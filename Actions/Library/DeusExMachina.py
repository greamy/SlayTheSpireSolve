from Entities.Player import Player
from Actions.Card import Card


class DeusExMachina(Card):
    def __init__(self):
        super().__init__("DeusExMachina", 1000, 0, 0, 0, 0, 0, True, "", None)