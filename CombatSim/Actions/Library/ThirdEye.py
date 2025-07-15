from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class ThirdEye(Card):
    def __init__(self, player: Player):
        super().__init__("ThirdEye", Card.Type.SKILL, 1, 0, 0, 7, 0, 0, False, False, player, None, id=76)
        self.description = "Gain 7 Block. Scry 3."
        self.scry = 3
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Gain 7(9) {{Block}}. {{Scry}} 3(5).
        ret = player.scry(self.scry, enemies, debug)

        return ret

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 9 Block. Scry 5."
        self.block = 9
        self.scry = 5
