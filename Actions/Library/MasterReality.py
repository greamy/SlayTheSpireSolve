from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class MasterReality(Card):
    def __init__(self):
        super().__init__("MasterReality", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever a card is created during combat, {{Upgrade}} it.
