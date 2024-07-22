from Entities.Player import Player
from Actions.Card import Card


class CutThroughFate(Card):
    def __init__(self):
        super().__init__("CutThroughFate", 1, 7, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.
