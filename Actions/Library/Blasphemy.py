from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Blasphemy(Card):
    def __init__(self):
        super().__init__("Blasphemy", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, "", Player.Stance.DIVINITY)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # (Retain.) Enter {{Divinity}}. Die next turn. {{Exhaust}}.
