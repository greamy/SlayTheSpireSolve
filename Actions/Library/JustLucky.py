from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class JustLucky(Card):
    def __init__(self):
        super().__init__("JustLucky", Card.Type.ATTACK, 0, 3, 1, 2, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Scry}} 1(2). Gain 2(3) {{Block}}. Deal 3(4) damage.
