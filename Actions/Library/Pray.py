from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Pray(Card):
    def __init__(self, player: Player):
        super().__init__("Pray", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Mantra}}. Shuffle an {{C|Insight}} into your draw pile.
