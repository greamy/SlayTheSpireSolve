from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Strike(Card):
    def __init__(self, player: Player):
        super().__init__("Strike", Card.Type.ATTACK, 1, 6, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 6(9) damage.

    def upgrade(self):
        super().upgrade()
        self.damage = 9
