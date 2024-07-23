from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Perseverance(Card):
    def __init__(self):
        super().__init__("Perseverance", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, True, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retain|Retained}}, increase its {{Block}} by 2(3).
