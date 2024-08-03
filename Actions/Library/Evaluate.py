from Actions.Library.Insight import Insight
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Evaluate(Card):
    def __init__(self, player: Player):
        super().__init__("Evaluate", Card.Type.SKILL, 1, 0, 0, 6, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.deck.draw_pile.append(Insight(player))
        player.deck.shuffle()
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.

    def upgrade(self):
        super().upgrade()
        self.block = 10
