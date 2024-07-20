from Entities.Player import Player
from Actions.Card import Card


class BattleHymn(Card):
    def __init__(self):
        super().__init__("BattleHymn", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
