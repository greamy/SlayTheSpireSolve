from Entities.Player import Player
from Actions.Card import Card


class SimmeringFury(Card):
    def __init__(self):
        super().__init__("SimmeringFury", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # At the start of your next turn, enter {{Wrath}} and draw 2(3) cards.
