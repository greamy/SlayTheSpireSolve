from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class ForeignInfluence(Card):
    def __init__(self, player: Player):
        super().__init__("ForeignInfluence", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, player, None, id=36)
        self.description = "Choose 1 of 3 attacks of any color to add to your hand. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Choose 1 of 3 Attacks of any color to add to your hand. (It costs 0 this turn.) {{Exhaust}}.

        return False

    def upgrade(self):
        super().upgrade()
        self.description = "Choose 1 of 3 attacks of any color to add to your hand. It costs 0 this turn. Exhaust."