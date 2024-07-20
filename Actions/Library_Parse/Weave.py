from Entities.Player import Player
from Actions.Card import Card


class Weave(Card):
    def __init__(self):
        super().__init__("Weave", 0, 4, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 4(6) damage. Whenever you {{Scry}}, return this from the discard pile to your Hand.
