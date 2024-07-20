from Entities.Player import Player
from Actions.Card import Card


class Omniscience(Card):
    def __init__(self):
        super().__init__("Omniscience", 4, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. Exhaust.
