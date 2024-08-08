from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Foresight(Card):
    def __init__(self, player: Player):
        super().__init__("Foresight", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the start of your turn, {{Scry}} 3(4).
