from Entities.Player import Player
from Actions.Card import Card


class WheelKick(Card):
    def __init__(self):
        super().__init__("WheelKick", 2, 15, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 15(20) damage. Draw 2 cards.
