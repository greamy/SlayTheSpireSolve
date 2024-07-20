from Entities.Player import Player
from Actions.Card import Card


class Worship(Card):
    def __init__(self):
        super().__init__("Worship", 2, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # ({{Retain}}.) Gain 5 {{Mantra}}.
