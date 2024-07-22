from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class WheelKick(Card):
    def __init__(self):
        super().__init__("WheelKick", 2, 15, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 15(20) damage. Draw 2 cards.
