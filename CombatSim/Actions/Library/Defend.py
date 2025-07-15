from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Defend(Card):
    def __init__(self, player: Player):
        super().__init__("Defend", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, False, player, None, id=20)
        self.description = "Gain 5 Block."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Gain 5(8) {{Block}}.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 8 Block."
        self.block = 8
