from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Protect(Card):
    def __init__(self, player: Player):
        super().__init__("Protect", Card.Type.SKILL, 2, 0, 0, 12, 0, 0, False, True, player, None, id=57)
        self.description = "Retain. Gain 12 Block."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 12(16) {{Block}}.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Gain 16 Block."
        self.block = 16
