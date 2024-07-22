from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Evaluate(Card):
    def __init__(self):
        super().__init__("Evaluate", Card.Type.SKILL, 1, 0, 0, 6, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.
