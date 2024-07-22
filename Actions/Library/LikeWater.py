from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class LikeWater(Card):
    def __init__(self):
        super().__init__("LikeWater", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, if you are in {{Calm}}, gain 5(7) {{Block}}.
