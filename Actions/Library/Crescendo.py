from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Crescendo(Card):
    def __init__(self):
        super().__init__("Crescendo", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, "", Player.Stance.WRATH)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Enter {{Wrath}}. {{Exhaust}}.
