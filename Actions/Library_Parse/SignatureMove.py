from Entities.Player import Player
from Actions.Card import Card


class SignatureMove(Card):
    def __init__(self):
        super().__init__("SignatureMove", 2, 30, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Can only be played if this is the only attack in your hand. Deal 30(40) damage.
