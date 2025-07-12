from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Scrawl(Card):
    def __init__(self, player: Player):
        super().__init__("Scrawl", Card.Type.SKILL, 1, 0, 0, 0, 10, 0, True, False, player, None, id=65)
        self.description = "Draw cards until your hand is full. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Draw cards until your hand is full. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 0
