from Entities.Player import Player
from Actions.Card import Card


class Brilliance(Card):
    def __init__(self):
        super().__init__("Brilliance", 1, 12, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 12(16) damage. Deals additional damage for all {{Mantra}} gained this combat.
