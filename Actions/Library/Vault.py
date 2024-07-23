from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Vault(Card):
    def __init__(self):
        super().__init__("Vault", Card.Type.SKILL, 3, 0, 0, 0, 0, 0, True, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Take an extra turn after this one. End your turn. {{Exhaust}}.
