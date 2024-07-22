from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class EmptyFist(Card):
    def __init__(self):
        super().__init__("EmptyFist", Card.Type.ATTACK, 1, 9, 1, 0, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 9(14) damage. Exit your {{Stance}}.
