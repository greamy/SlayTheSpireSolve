from Entities.Player import Player
from Actions.Card import Card


class ReachHeaven(Card):
    def __init__(self):
        super().__init__("ReachHeaven", 2, 10, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 10(15) damage. Shuffle a {{C|Through Violence}} into your draw pile.
