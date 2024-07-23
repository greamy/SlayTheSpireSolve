from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Swivel(Card):
    def __init__(self):
        super().__init__("Swivel", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 8(11) {{Block}}. The next Attack you play costs 0.
