from Entities.Player import Player
from Actions.Card import Card


class Collect(Card):
    def __init__(self):
        super().__init__("Collect", 0, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.
