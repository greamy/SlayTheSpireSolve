from Entities.Player import Player
from Actions.Card import Card


class WindmillStrike(Card):
    def __init__(self):
        super().__init__("WindmillStrike", 2, 7, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 7(10) damage. Whenever this card is {{Retain|Retained}}, increase its damage by 4(5).
