from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Protect(Card):
    def __init__(self, player: Player):
        super().__init__("Protect", Card.Type.SKILL, 2, 0, 0, 12, 0, 0, False, True, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 12(16) {{Block}}.
