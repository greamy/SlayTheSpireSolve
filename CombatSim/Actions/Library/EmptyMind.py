from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class EmptyMind(Card):
    def __init__(self, player: Player):
        super().__init__("EmptyMind", Card.Type.SKILL, 1, 0, 0, 0, 2, 0, False, False, player, Player.Stance.NONE, id=26)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Exit your {{Stance}}. Draw 2(3) cards.

    def upgrade(self):
        super().upgrade()
        self.draw = 3
