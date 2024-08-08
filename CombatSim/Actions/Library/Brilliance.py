from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Brilliance(Card):
    def __init__(self, player: Player):
        super().__init__("Brilliance", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        self.damage = 12 + player.mantra
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 12(16) damage. Deals additional damage for all {{Mantra}} gained this combat.

    def upgrade(self):
        super().upgrade()
        self.damage = 16
