from Entities.Player import Player
from Actions.Card import Card


class JustLucky(Card):
    def __init__(self):
        super().__init__("JustLucky", 0, 3, 1, 2, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Scry}} 1(2). Gain 2(3) {{Block}}. Deal 3(4) damage.
