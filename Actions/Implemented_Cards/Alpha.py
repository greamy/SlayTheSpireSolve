from Actions.Card import Card
from Actions.Implemented_Cards.Beta import Beta
from Entities.Enemy import Enemy
from Entities.Player import Player


class Alpha(Card):
    def __init__(self):
        super().__init__("Alpha", 1, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, enemy, enemies, debug)
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Beta())
        player.deck.shuffle()
