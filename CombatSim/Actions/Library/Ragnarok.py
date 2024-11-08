from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class Ragnarok(Card):
    def __init__(self, player: Player):
        super().__init__("Ragnarok", Card.Type.ATTACK, 3, 5, 1, 0, 0, 0, False, False, player, None, id=58)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Deal 5(6) damage to a random enemy 5(6) times.
        for i in range(self.attacks):
            enemy = random.choice(enemies)
            super().play(player, player_list, enemy, enemies, debug)


    def upgrade(self):
        super().upgrade()
        self.damage = 6
        self.attacks = 6
