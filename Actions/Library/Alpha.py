from Entities.Player import Player
from Actions.Card import Card
from Actions.Library.Beta import Beta


class Alpha(Card):
    def __init__(self):
        super().__init__("Alpha", 1, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Beta())
        player.deck.shuffle()
