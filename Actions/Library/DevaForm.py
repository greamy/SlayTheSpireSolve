from Entities.Player import Player
from Actions.Card import Card


class DevaForm(Card):
    def __init__(self):
        super().__init__("DevaForm", 3, 0, 0, 0, 0, 0, False, "", None)