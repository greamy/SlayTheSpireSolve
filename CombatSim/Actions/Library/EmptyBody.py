from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class EmptyBody(Card):
    def __init__(self, player: Player):
        super().__init__("EmptyBody", Card.Type.SKILL, 1, 0, 0, 7, 0, 0, False, False, player, Player.Stance.NONE)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 7(10) {{Block}}. Exit your {{Stance}}.

    def upgrade(self):
        super().upgrade()
        self.block = 10
