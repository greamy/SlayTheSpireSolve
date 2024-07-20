from Entities.Player import Player
from Actions.Card import Card


class Ragnarok(Card):
    def __init__(self):
        super().__init__("Ragnarok", 3, 5, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 5(6) damage to a random enemy 5(6) times.
