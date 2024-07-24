from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Expunger(Card):
    def __init__(self, attacks):
        super().__init__("Expunger", Card.Type.SKILL, 0, 9, attacks, 0, 0, 0, True, False, "", None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Deal 9 damage X times.
