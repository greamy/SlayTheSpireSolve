from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Consecrate(Card):
    def __init__(self):
        super().__init__("Consecrate", Card.Type.ATTACK, 0, 5, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 5(8) damage to ALL enemies.
