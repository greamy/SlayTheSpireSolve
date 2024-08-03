from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Weave(Card):
    def __init__(self, player: Player):
        super().__init__("Weave", Card.Type.ATTACK, 0, 4, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 4(6) damage. Whenever you {{Scry}}, return this from the discard pile to your Hand.
