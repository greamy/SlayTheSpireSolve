from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Study(Card):
    def __init__(self, player: Player):
        super().__init__("Study", Card.Type.POWER, 2, 0, 0, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, shuffle an {{C|Insight}} into your draw pile.
