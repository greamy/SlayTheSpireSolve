from Entities.Player import Player
from Actions.Card import Card


class PressurePoints(Card):
    def __init__(self):
        super().__init__("PressurePoints", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Apply 8(11) Mark. ALL enemies lose HP equal to their Mark.
