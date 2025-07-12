from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Conclude(Card):
    def __init__(self, player: Player):
        super().__init__("Conclude", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, False, False, player, None, id=10)
        self.description = "Deal 12 damage to ALL enemies. End your turn."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        for enemy in enemies:
            super().play(player, player_list, enemy, enemies, debug)
        # Deal 12(16) damage to ALL enemies. End your turn.
        player.turn_over = True

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 16 damage to ALL enemies. End your turn."
        self.damage = 16
