from Entities.Player import Player
from Actions.Card import Card


class CarveReality(Card):
    def __init__(self):
        super().__init__("CarveReality", 1, 6, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 6(10) damage. Add a {{C|Smite}} into your hand.
