from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Worship(Card):
    def __init__(self):
        super().__init__("Worship", 2, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # ({{Retain}}.) Gain 5 {{Mantra}}.
