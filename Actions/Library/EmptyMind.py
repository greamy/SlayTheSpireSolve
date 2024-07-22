from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class EmptyMind(Card):
    def __init__(self):
        super().__init__("EmptyMind", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Exit your {{Stance}}. Draw 2(3) cards.
