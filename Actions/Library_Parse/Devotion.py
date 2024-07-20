from Entities.Player import Player
from Actions.Card import Card


class Devotion(Card):
    def __init__(self):
        super().__init__("Devotion", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # At the start of your turn, gain 2(3) {{Mantra}}.
