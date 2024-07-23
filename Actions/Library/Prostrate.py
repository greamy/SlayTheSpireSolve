from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Prostrate(Card):
    def __init__(self):
        super().__init__("Prostrate", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.
