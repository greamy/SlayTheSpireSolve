from Entities.Player import Player
from Actions.Card import Card


class Prostrate(Card):
    def __init__(self):
        super().__init__("Prostrate", 0, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.
