from Entities.Player import Player
from Actions.Card import Card


class DevaForm(Card):
    def __init__(self):
        super().__init__("DevaForm", 3, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)
