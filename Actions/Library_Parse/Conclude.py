from Entities.Player import Player
from Actions.Card import Card


class Conclude(Card):
    def __init__(self):
        super().__init__("Conclude", 1, 12, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 12(16) damage to ALL enemies. End your turn.
