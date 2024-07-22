from Entities.Player import Player
from Actions.Card import Card


class Wallop(Card):
    def __init__(self):
        super().__init__("Wallop", 2, 9, 1, , 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 9(12) damage. Gain {{Block}} equal to unblocked damage dealt.
