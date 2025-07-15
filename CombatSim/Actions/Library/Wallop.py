from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Wallop(Card):
    def __init__(self, player: Player):
        super().__init__("Wallop", Card.Type.ATTACK, 2, 9, 1, 0, 0, 0, False, False, player, None, id=81)
        self.description = "Deal 9 damage. Gain Block equal to unblocked damage dealt."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Deal 9(12) damage. Gain {{Block}} equal to unblocked damage dealt.
        enemy_block = target_enemy.block
        super().play(player, player_list, target_enemy, enemies, debug)
        player.gain_block(self.one_attack_damage*self.attacks - enemy_block, enemies, debug)

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 12 damage. Gain Block equal to unblocked damage dealt."
        self.damage = 12
