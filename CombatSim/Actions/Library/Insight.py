from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Insight(Card):
    def __init__(self, player: Player):
        super().__init__("Insight", Card.Type.SKILL, 0, 0, 0, 0, 2, 0, True, True, player, None, id=41)
        self.description = "Retain. Draw 2 cards. Exhaust."

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)

        # {{Retain}} Draw 2(3) cards}. {{Exhaust}}

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Draw 3 cards. Exhaust."
        self.draw = 3
