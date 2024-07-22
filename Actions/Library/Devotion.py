from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Devotion(Card):
    def __init__(self):
        super().__init__("Devotion", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the start of your turn, gain 2(3) {{Mantra}}.
