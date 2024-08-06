from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Vault(Card):
    def __init__(self, player: Player):
        super().__init__("Vault", Card.Type.SKILL, 3, 0, 0, 0, 0, 0, True, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Take an extra turn after this one. End your turn. {{Exhaust}}.
        super().play(player, target_enemy, enemies, debug)
        player.end_turn(enemies, debug)
        player.start_turn(enemies, debug)