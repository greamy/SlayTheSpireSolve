from Entities.Player import Player
from Actions.Card import Card


class SandsofTime(Card):
    def __init__(self):
        super().__init__("SandsofTime", 4, 20, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 20(26) damage. Whenever this card is {{Retain|Retained}}, lower its cost by 1.
