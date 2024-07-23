from Actions.Card import Card
from Actions.Library.Omega import Omega
from Entities.Enemy import Enemy
from Entities.Player import Player


class Beta(Card):
    def __init__(self):
        super().__init__("Beta", Card.Type.SKILL,2, 0, 0, 0, 0, 0, True, False,"", None)

    def play(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, enemy, enemies, debug)
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Omega())
        player.deck.shuffle()
