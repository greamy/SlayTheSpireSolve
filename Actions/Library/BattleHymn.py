from Entities.Player import Player
from Actions.Card import Card


class BattleHymn(Card):
    def __init__(self):
        super().__init__("BattleHymn", 1, 0, 0, 0, 0, 0, False, "", None)