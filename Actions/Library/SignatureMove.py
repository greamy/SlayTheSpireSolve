from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class SignatureMove(Card):
    def __init__(self):
        super().__init__("SignatureMove", Card.Type.ATTACK, 2, 30, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Can only be played if this is the only attack in your hand. Deal 30(40) damage.
