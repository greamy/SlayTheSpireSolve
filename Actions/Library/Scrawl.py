from Entities.Player import Player
from Actions.Card import Card


class Scrawl(Card):
    def __init__(self):
        super().__init__("Scrawl", 1, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Draw cards until your hand is full. {{Exhaust}}.
