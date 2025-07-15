
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Miracle(Card):
    def __init__(self, player: Player):
        super().__init__("Miracle", Card.Type.SKILL, -1, 0, 0, 0, 0, 0, True, True, player, None, id=49)
        self.description = "Retain. Gain 1 energy. Exhaust."

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Retain. Gain 1(2) energy. {{Exhaust}}.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Gain 2 energy. Exhaust."
        self.energy = -2
