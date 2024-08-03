from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Sanctity(Card):
    def __init__(self, player: Player):
        super().__init__("Sanctity", Card.Type.SKILL, 1, 0, 0, 6, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 6(9) {{Block}}. If the previous card played was a Skill, draw 2 card.
