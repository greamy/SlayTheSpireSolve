from Entities.Player import Player
from Actions.Card import Card


class Establishment(Card):
    def __init__(self):
        super().__init__("Establishment", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # ({{Innate}}.) Whenever a card is {{Retain|Retained}}, lower its cost by 1.
