from Entities.Player import Player
from Actions.Card import Card


class WreathofFlame(Card):
    def __init__(self):
        super().__init__("WreathofFlame", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Your next Attack deals 5(8) additional damage.
