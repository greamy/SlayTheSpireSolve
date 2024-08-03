from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Defend(Card):
    def __init__(self, player: Player):
        super().__init__("Defend", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Gain 5(8) {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.block = 8
