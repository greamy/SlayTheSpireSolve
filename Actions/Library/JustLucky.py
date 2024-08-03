from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class JustLucky(Card):
    def __init__(self, player: Player):
        super().__init__("JustLucky", Card.Type.ATTACK, 0, 3, 1, 2, 0, 0, False, False, player, None)
        self.scry = 1
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Scry}} 1(2). Gain 2(3) {{Block}}. Deal 3(4) damage.
        player.scry(self.scry)

    def upgrade(self):
        super().upgrade()
        self.damage = 4
        self.block = 3
        self.scry = 2
