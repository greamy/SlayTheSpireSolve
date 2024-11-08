from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Slimed(Card):
    def __init__(self, player: Player):
        super().__init__("Slimed", Card.Type.STATUS, 1, 0, 0, 0, 0, 0, True, False, player, None, id=68)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # {{Exhaust}}
        super().play(player, player_list, target_enemy, enemies, debug)
