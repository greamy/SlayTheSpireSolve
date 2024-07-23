from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Brilliance(Card):
    def __init__(self):
        super().__init__("Brilliance", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        self.damage = 12 + player.mantra
        super().play(player, target_enemy, enemies, debug)
        # Deal 12(16) damage. Deals additional damage for all {{Mantra}} gained this combat.

    def upgrade(self):
        super().upgrade()
        self.damage = 16
