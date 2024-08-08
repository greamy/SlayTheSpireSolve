from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Expunger(Card):
    def __init__(self, player: Player, attacks):
        super().__init__("Expunger", Card.Type.ATTACK, 0, 9, attacks, 0, 0, 0, True, False, player, None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Deal 9 damage X times.