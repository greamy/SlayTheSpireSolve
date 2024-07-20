from Entities.Player import Player
from Actions.Card import Card


class Pray(Card):
    def __init__(self):
        super().__init__("Pray", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Mantra}}. Shuffle an {{C|Insight}} into your draw pile.
