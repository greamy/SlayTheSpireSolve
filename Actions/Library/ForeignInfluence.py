from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class ForeignInfluence(Card):
    def __init__(self):
        super().__init__("ForeignInfluence", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Choose 1 of 3 Attacks of any color to add to your hand. (It costs 0 this turn.) {{Exhaust}}.
