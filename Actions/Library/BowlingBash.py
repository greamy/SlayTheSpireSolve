from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class BowlingBash(Card):
    def __init__(self):
        super().__init__("BowlingBash", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        self.attacks = len(enemies)
        super().play(player, target_enemy, enemies, debug)
        # Deal 7(10) damage for each enemy in combat.

    def upgrade(self):
        super().upgrade()
        self.damage = 10
