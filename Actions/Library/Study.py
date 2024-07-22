from Entities.Player import Player
from Actions.Card import Card


class Study(Card):
    def __init__(self):
        super().__init__("Study", 2, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # At the end of your turn, shuffle an {{C|Insight}} into your draw pile.
