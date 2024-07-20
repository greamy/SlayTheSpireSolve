from Entities.Player import Player
from Actions.Card import Card


class Meditate(Card):
    def __init__(self):
        super().__init__("Meditate", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.CALM)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
