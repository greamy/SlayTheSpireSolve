from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class Ragnarok(Card):
    def __init__(self, player: Player):
        super().__init__("Ragnarok", Card.Type.ATTACK, 3, 5, 1, 0, 0, 0, False, False, player, None, id=58)
        self.description = "Deal 5 damage to a random enemy 5 times."
        self.num_attacks = 5
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Deal 5(6) damage to a random enemy 5(6) times.
        for i in range(self.num_attacks):
            enemy = random.choice(enemies)
            super().play(player, player_list, enemy, enemies, debug)

        return True


    def upgrade(self):
        super().upgrade()
        self.description = "Deal 6 damage to a random enemy 6 times."
        self.damage = 6
        self.attacks = 6
