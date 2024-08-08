from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Omega import Omega
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player


class Beta(Card):
    def __init__(self, player: Player):
        super().__init__("Beta", Card.Type.SKILL,2, 0, 0, 0, 0, 0, True, False, player, None)

    def play(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, enemy, enemies, debug)
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Omega(player))
        player.deck.shuffle()

    def upgrade(self):
        super().upgrade()
        self.energy = 1
