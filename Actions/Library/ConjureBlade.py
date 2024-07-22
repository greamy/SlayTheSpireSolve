from Entities.Player import Player
from Actions.Card import Card


class ConjureBlade(Card):
    def __init__(self):
        super().__init__("ConjureBlade", 0, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Shuffle an {{C|Expunger}} with X(+1) into your draw pile. {{Exhaust}}.
