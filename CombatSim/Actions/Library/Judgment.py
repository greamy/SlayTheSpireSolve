from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Judgment(Card):
    def __init__(self, player: Player):
        super().__init__("Judgment", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.death = 30

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # If the enemy has 30(40) or less HP, set their HP to 0.
        if target_enemy.health <= self.death:
            target_enemy.health = 0

    def upgrade(self):
        super().upgrade()
        self.death = 40
