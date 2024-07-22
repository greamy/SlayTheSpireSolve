from Entities.Player import Player
from Actions.Card import Card


class ForeignInfluence(Card):
    def __init__(self):
        super().__init__("ForeignInfluence", 0, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Choose 1 of 3 Attacks of any color to add to your hand. (It costs 0 this turn.) {{Exhaust}}.
