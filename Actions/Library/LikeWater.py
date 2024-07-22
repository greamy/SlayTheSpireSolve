from Entities.Player import Player
from Actions.Card import Card


class LikeWater(Card):
    def __init__(self):
        super().__init__("LikeWater", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # At the end of your turn, if you are in {{Calm}}, gain 5(7) {{Block}}.
