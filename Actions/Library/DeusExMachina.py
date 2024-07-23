from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class DeusExMachina(Card):
    def __init__(self):
        super().__init__("DeusExMachina", Card.Type.SKILL, 1000, 0, 0, 0, 0, 0, True, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Unplayable}}. When you draw this card, add 2(3) {{C|Miracle|Miracles}} into your hand. {{Exhaust}}.
