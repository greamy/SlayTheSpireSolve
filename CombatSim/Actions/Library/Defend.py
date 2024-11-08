from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Defend(Card):
    def __init__(self, player: Player):
        super().__init__("Defend", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, False, player, None, id=20)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Gain 5(8) {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.block = 8
