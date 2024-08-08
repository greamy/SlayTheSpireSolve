from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Vigilance(Card):
    def __init__(self, player: Player):
        super().__init__("Vigilance", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, False, player, Player.Stance.CALM)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Enter {{Calm}}. Gain 8(12) {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.block = 12
