from Entities.Player import Player
from Actions.Card import Card


class Tantrum(Card):
    def __init__(self):
        super().__init__("Tantrum", 1, 3 damage 3, 1, 0, 0, 0, False, "", Player.Stance.WRATH)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 3 damage 3(4) times. Enter {{Wrath}}. Shuffle this card into your draw pile.
