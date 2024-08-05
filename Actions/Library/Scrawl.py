from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Scrawl(Card):
    def __init__(self, player: Player):
        super().__init__("Scrawl", Card.Type.SKILL, 1, 0, 0, 0, 10, 0, True, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Draw cards until your hand is full. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 0
