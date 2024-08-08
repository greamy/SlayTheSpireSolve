from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class FearNoEvil(Card):
    def __init__(self, player: Player):
        super().__init__("FearNoEvil", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 8(11) damage. If the enemy intends to Attack, enter {{Calm}}.
        if target_enemy.intent.damage > 0:
            player.set_stance(Player.Stance.CALM)

    def upgrade(self):
        super().upgrade()
        self.damage = 11
