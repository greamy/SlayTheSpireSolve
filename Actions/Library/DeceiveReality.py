from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class DeceiveReality(Card):
    def __init__(self):
        super().__init__("DeceiveReality", Card.Type.SKILL, 1, 0, 0, 4, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.
