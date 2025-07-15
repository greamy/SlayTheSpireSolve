from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Consecrate(Card):
    def __init__(self, player: Player):
        super().__init__("Consecrate", Card.Type.ATTACK, 0, 5, 1, 0, 0, 0, False, False, player, None, id=12)
        self.description = "Deal 5 damage to ALL enemies."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        for enemy in enemies:
            super().play(player, player_list, enemy, enemies, debug)
        # Deal 5(8) damage to ALL enemies.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 8 damage to ALL enemies."
        self.damage = 8
