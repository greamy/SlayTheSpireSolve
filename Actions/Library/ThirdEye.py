from Entities.Player import Player
from Actions.Card import Card


class ThirdEye(Card):
    def __init__(self):
        super().__init__("ThirdEye", 1, 0, 0, 7, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 7(9) {{Block}}. {{Scry}} 3(5).
