from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class JustLucky(Card):
    def __init__(self, player: Player):
        super().__init__("JustLucky", Card.Type.ATTACK, 0, 3, 1, 2, 0, 0, False, False, player, None, id=43)
        self.description = "Scry 1. Gain 2 Block. Deal 3 damage."
        self.scry = 1
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # {{Scry}} 1(2). Gain 2(3) {{Block}}. Deal 3(4) damage.
        player.scry(self.scry, enemies, debug)

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Scry 2. Gain 3 Block. Deal 4 damage."
        self.damage = 4
        self.block = 3
        self.scry = 2
