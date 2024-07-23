from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Conclude(Card):
    def __init__(self):
        super().__init__("Conclude", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 12(16) damage to ALL enemies. End your turn.
