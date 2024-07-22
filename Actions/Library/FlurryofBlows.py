from Entities.Player import Player
from Actions.Card import Card


class FlurryofBlows(Card):
    def __init__(self):
        super().__init__("FlurryofBlows", 0, 4, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.
