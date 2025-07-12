from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Vigilance(Card):
    def __init__(self, player: Player):
        super().__init__("Vigilance", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, False, player, Player.Stance.CALM, id=80)
        self.description = "Enter Calm. Gain 8 Block."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Enter {{Calm}}. Gain 8(12) {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.description = "Enter Calm. Gain 12 Block."
        self.block = 12
