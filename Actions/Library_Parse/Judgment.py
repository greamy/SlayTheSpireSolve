from Entities.Player import Player
from Actions.Card import Card


class Judgment(Card):
    def __init__(self):
        super().__init__("Judgment", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # If the enemy has 30(40) or less HP, set their HP to 0.
