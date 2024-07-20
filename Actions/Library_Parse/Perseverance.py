from Entities.Player import Player
from Actions.Card import Card


class Perseverance(Card):
    def __init__(self):
        super().__init__("Perseverance", 1, 0, 0, 5, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retain|Retained}}, increase its {{Block}} by 2(3).
