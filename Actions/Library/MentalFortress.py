from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class MentalFortress(Card):
    def __init__(self):
        super().__init__("MentalFortress", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever you switch {{Stance|Stances}}, gain 4(6) {{Block}}.
