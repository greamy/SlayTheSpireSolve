from Entities.Player import Player
from Actions.Card import Card


class EmptyFist(Card):
    def __init__(self):
        super().__init__("EmptyFist", 1, 9, 1, 0, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 9(14) damage. Exit your {{Stance}}.
