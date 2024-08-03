from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Insight(Card):
    def __init__(self, player: Player):
        super().__init__("Insight", Card.Type.SKILL, 0, 0, 0, 0, 2, 0, True, True, player, None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)

        # {{Retain}} Draw 2(3) cards}. {{Exhaust}}

    def upgrade(self):
        super().upgrade()
        self.draw = 3
