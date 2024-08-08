from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class CutThroughFate(Card):
    def __init__(self, player: Player):
        super().__init__("CutThroughFate", Card.Type.ATTACK, 1, 7, 1, 0, 1, 0, False, False, player, None)
        self.scry_amount = 2
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        player.scry(self.scry_amount, enemies, debug)
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.

    def upgrade(self):
        super().upgrade()
        self.damage = 9
        self.scry_amount = 3
