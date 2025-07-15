from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class ThroughViolence(Card):
    def __init__(self, player: Player):
        super().__init__("ThroughViolence", Card.Type.ATTACK, 0, 20, 1, 0, 0, 0, True, True, player, None, id=77)
        self.description = "Retain. Deal 20 damage. Exhaust."

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}} Deal 20(30) damage. {{Exhaust}}

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Deal 30 damage. Exhaust."
        self.damage = 30
