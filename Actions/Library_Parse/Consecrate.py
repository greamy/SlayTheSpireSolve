from Entities.Player import Player
from Actions.Card import Card


class Consecrate(Card):
    def __init__(self):
        super().__init__("Consecrate", 0, 5, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 5(8) damage to ALL enemies.
