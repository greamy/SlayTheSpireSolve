from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class DevaForm(Card):
    def __init__(self):
        super().__init__("DevaForm", 3, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)
