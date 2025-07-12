from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class WheelKick(Card):
    def __init__(self, player: Player):
        super().__init__("WheelKick", Card.Type.ATTACK, 2, 15, 1, 0, 2, 0, False, False, player, None, id=84)
        self.description = "Deal 15 damage. Draw 2 cards."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 15(20) damage. Draw 2 cards.

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 20 damage. Draw 2 cards."
        self.damage = 20
