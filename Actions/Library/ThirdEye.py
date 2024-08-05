from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class ThirdEye(Card):
    def __init__(self, player: Player):
        super().__init__("ThirdEye", Card.Type.SKILL, 1, 0, 0, 7, 0, 0, False, False, player, None)
        self.scry = 3
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Gain 7(9) {{Block}}. {{Scry}} 3(5).
        player.scry(self.scry, enemies, debug)

    def upgrade(self):
        super().upgrade()
        self.block = 9
        self.scry = 5
