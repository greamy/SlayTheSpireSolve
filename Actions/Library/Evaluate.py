from Entities.Player import Player
from Actions.Card import Card


class Evaluate(Card):
    def __init__(self):
        super().__init__("Evaluate", 1, 0, 0, 6, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.
