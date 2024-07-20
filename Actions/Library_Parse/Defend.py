from Entities.Player import Player
from Actions.Card import Card


class Defend(Card):
    def __init__(self):
        super().__init__("Defend", 1, 0, 0, 5, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 5(8) {{Block}}.
