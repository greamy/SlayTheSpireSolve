from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Nirvana(Card):
    def __init__(self, player: Player):
        super().__init__("Nirvana", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever you {{Scry}}, gain 3(4) {{Block}}.
