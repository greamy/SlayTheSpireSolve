from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class SashWhip(Card):
    def __init__(self):
        super().__init__("SashWhip", 1, 8, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 8(10) damage. If the last card played this combat was an Attack, apply 1(2) {{Weak}}.
