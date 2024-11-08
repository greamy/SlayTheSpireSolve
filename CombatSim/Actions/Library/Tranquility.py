from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Tranquility(Card):
    def __init__(self, player: Player):
        super().__init__("Tranquility", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, True, player, Player.Stance.CALM, id=78)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Enter {{Calm}}. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 0
