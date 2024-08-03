from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class ThirdEye(Card):
    def __init__(self, player: Player):
        super().__init__("ThirdEye", Card.Type.SKILL, 1, 0, 0, 7, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 7(9) {{Block}}. {{Scry}} 3(5).
