from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class ReachHeaven(Card):
    def __init__(self, player: Player):
        super().__init__("ReachHeaven", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 10(15) damage. Shuffle a {{C|Through Violence}} into your draw pile.
