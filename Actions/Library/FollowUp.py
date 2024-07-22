from Entities.Player import Player
from Actions.Card import Card


class FollowUp(Card):
    def __init__(self):
        super().__init__("FollowUp", 1, 7, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 7(11) damage. If the previous card played was an Attack, gain 1 {{Energy}}.
