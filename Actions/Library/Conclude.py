from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Conclude(Card):
    def __init__(self, player: Player):
        super().__init__("Conclude", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        for enemy in enemies:
            super().play(player, enemy, enemies, debug)
        # Deal 12(16) damage to ALL enemies. End your turn.
        player.turn_over = True

    def upgrade(self):
        super().upgrade()
        self.damage = 16
