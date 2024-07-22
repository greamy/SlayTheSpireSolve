from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Vigilance(Card):
    def __init__(self):
        super().__init__("Vigilance", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, "", Player.Stance.CALM)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Enter {{Calm}}. Gain 8(12) {{Block}}.
