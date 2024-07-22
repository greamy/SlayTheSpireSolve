from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Scrawl(Card):
    def __init__(self):
        super().__init__("Scrawl", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Draw cards until your hand is full. {{Exhaust}}.
