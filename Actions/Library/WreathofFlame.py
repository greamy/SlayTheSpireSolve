from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class WreathofFlame(Card):
    def __init__(self):
        super().__init__("WreathofFlame", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Your next Attack deals 5(8) additional damage.
