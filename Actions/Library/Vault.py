from Entities.Player import Player
from Actions.Card import Card


class Vault(Card):
    def __init__(self):
        super().__init__("Vault", 3, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Take an extra turn after this one. End your turn. {{Exhaust}}.
