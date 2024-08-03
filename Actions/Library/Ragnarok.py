from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Ragnarok(Card):
    def __init__(self, player: Player):
        super().__init__("Ragnarok", Card.Type.ATTACK, 3, 5, 5, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 5(6) damage to a random enemy 5(6) times.
