from Entities.Player import Player
from Actions.Card import Card
from Actions.Library.Omega import Omega


class Beta(Card):
    def __init__(self):
        super().__init__("Beta", 2, 0, 0, 0, 0, 0, True, "", None)

    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Omega())
        player.deck.shuffle()
