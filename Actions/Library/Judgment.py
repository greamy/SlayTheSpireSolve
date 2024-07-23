from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Judgment(Card):
    def __init__(self):
        super().__init__("Judgment", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # If the enemy has 30(40) or less HP, set their HP to 0.
