from Entities.Player import Player
from Actions.Card import Card


class SpiritShield(Card):
    def __init__(self):
        super().__init__("SpiritShield", 2, 0, 0, 3, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Block}} for each card in your hand.
