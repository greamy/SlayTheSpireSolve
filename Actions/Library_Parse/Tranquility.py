from Entities.Player import Player
from Actions.Card import Card


class Tranquility(Card):
    def __init__(self):
        super().__init__("Tranquility", 1, 0, 0, 0, 0, 0, True, "", Player.Stance.CALM)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Retain}}. Enter {{Calm}}. {{Exhaust}}.
