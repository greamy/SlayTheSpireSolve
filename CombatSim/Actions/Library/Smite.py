from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Smite(Card):
    def __init__(self, player: Player):
        super().__init__("Smite", Card.Type.ATTACK, 1, 12, 1, 0, 0, 0, True, True, player, None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Retain. Deal 12 damage. {{Exhaust}}.
