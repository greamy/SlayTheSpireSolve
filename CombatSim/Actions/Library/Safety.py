from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Safety(Card):
    def __init__(self, player: Player):
        super().__init__("Safety", Card.Type.SKILL, 1, 0, 0, 12, 0, 0, True, True, player, None, id=61)
        self.description = "Retain. Gain 12 Block. Exhaust."

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 12(16) {{Block}} Exhaust.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Gain 16 Block. Exhaust."
        self.block = 16
