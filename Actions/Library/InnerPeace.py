from Entities.Player import Player
from Actions.Card import Card


class InnerPeace(Card):
    def __init__(self):
        super().__init__("InnerPeace", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.CALM)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
