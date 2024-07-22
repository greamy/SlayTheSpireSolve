from Entities.Player import Player
from Actions.Card import Card


class Rushdown(Card):
    def __init__(self):
        super().__init__("Rushdown", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Whenever you enter {{Wrath}}, draw 2 cards.
