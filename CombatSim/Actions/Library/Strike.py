from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Strike(Card):
    def __init__(self, player: Player):
        super().__init__("Strike", Card.Type.ATTACK, 1, 6, 1, 0, 0, 0, False, False, player, None, id=71)
        self.description = "Deal 6 damage."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 6(9) damage.

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 9 damage."
        self.damage = 9
