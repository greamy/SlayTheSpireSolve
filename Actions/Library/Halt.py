from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Halt(Card):
    def __init__(self):
        super().__init__("Halt", Card.Type.SKILL, 0, 0, 0, 3, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Block}}. {{Wrath}}: Gain 9(14) additional {{Block}}.
