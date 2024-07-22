from Entities.Player import Player
from Actions.Card import Card


class BowlingBash(Card):
    def __init__(self):
        super().__init__("BowlingBash", 1, 7, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 7(10) damage for each enemy in combat.
