from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class CrushJoints(Card):
    def __init__(self):
        super().__init__("CrushJoints", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.
