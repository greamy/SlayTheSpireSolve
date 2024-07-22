from Entities.Player import Player
from Actions.Card import Card


class FlyingSleeves(Card):
    def __init__(self):
        super().__init__("FlyingSleeves", 1, 4, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 4(6) damage twice.
