from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Indignation(Card):
    def __init__(self):
        super().__init__("Indignation", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.
