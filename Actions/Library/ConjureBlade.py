from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class ConjureBlade(Card):
    def __init__(self):
        super().__init__("ConjureBlade", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Shuffle an {{C|Expunger}} with X(+1) into your draw pile. {{Exhaust}}.
