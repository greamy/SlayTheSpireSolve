from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class EmptyBody(Card):
    def __init__(self):
        super().__init__("EmptyBody", Card.Type.SKILL, 1, 0, 0, 7, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 7(10) {{Block}}. Exit your {{Stance}}.
