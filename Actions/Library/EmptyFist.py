from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class EmptyFist(Card):
    def __init__(self, player: Player):
        super().__init__("EmptyFist", Card.Type.ATTACK, 1, 9, 1, 0, 0, 0, False, False, player, Player.Stance.NONE)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Deal 9(14) damage. Exit your {{Stance}}.

    def upgrade(self):
        super().upgrade()
        self.damage = 14
