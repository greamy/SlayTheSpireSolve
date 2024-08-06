from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class BowlingBash(Card):
    def __init__(self, player: Player):
        super().__init__("BowlingBash", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        self.attacks = len(enemies)
        super().play(player, target_enemy, enemies, debug)
        # Deal 7(10) damage for each enemy in combat.

    def upgrade(self):
        super().upgrade()
        self.damage = 10
