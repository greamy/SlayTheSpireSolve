from Entities.Player import Player
from Actions.Card import Card


class FearNoEvil(Card):
    def __init__(self):
        super().__init__("FearNoEvil", 1, 8, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 8(11) damage. If the enemy intends to Attack, enter {{Calm}}.
