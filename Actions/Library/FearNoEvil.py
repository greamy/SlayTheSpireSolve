from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class FearNoEvil(Card):
    def __init__(self):
        super().__init__("FearNoEvil", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 8(11) damage. If the enemy intends to Attack, enter {{Calm}}.
        if target_enemy.intent.damage > 0:
            player.set_stance(Player.Stance.CALM)

    def upgrade(self):
        super().upgrade()
        self.damage = 11
