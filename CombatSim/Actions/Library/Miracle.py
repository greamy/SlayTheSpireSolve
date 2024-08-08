
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Miracle(Card):
    def __init__(self, player: Player):
        super().__init__("Miracle", Card.Type.SKILL, -1, 0, 0, 0, 0, 0, True, True, player, None)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Retain. Gain 1(2) energy. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = -2
