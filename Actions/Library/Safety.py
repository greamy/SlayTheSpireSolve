from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Safety(Card):
    def __init__(self):
        super().__init__("Safety", Card.Type.SKILL, 1, 0, 0, 12, 0, 0, True, True, "", None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 12(16) {{Block}}.

    def upgrade(self):
        self.block = 16
