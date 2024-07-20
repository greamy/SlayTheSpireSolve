from Entities.Player import Player
from Actions.Card import Card


class WaveoftheHand(Card):
    def __init__(self):
        super().__init__("WaveoftheHand", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Whenever you gain {{Block}} this turn, apply 1(2) {{Weak}} to ALL enemies.
