from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class PressurePoints(Card):
    def __init__(self, player: Player):
        super().__init__("PressurePoints", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.card_mark = 8
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        target_enemy.mark += self.card_mark
        for enemy in enemies:
            enemy.health -= enemy.mark

        # Apply 8(11) Mark. ALL enemies lose HP equal to their Mark.

    def upgrade(self):
        super().upgrade()
        self.card_mark = 11

