from Entities.Player import Player
from Actions.Card import Card


class Swivel(Card):
    def __init__(self):
        super().__init__("Swivel", 2, 0, 0, 8, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 8(11) {{Block}}. The next Attack you play costs 0.
