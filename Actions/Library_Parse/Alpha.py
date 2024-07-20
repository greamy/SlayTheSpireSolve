from Entities.Player import Player
from Actions.Card import Card


class Alpha(Card):
    def __init__(self):
        super().__init__("Alpha", 1, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
