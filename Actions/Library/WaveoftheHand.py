from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class WaveoftheHand(Card):
    def __init__(self):
        super().__init__("WaveoftheHand", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever you gain {{Block}} this turn, apply 1(2) {{Weak}} to ALL enemies.
