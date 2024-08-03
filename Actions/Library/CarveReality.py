from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Library.Smite import Smite


class CarveReality(Card):
    def __init__(self, player: Player):
        super().__init__("CarveReality", Card.Type.ATTACK, 1, 6, 1, 0, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        player.deck.hand.append(Smite(player))
        # TODO: Implement the following:
        # Deal 6(10) damage. Add a {{C|Smite}} into your hand.

    def upgrade(self):
        super().upgrade()
        self.damage = 10
