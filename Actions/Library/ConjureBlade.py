from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Library.Expunger import Expunger


class ConjureBlade(Card):
    def __init__(self):
        super().__init__("ConjureBlade", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, "", None)
        self.x_modifier = 0

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Shuffle an {{C|Expunger}} with X(+1) into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Expunger(player.energy + self.x_modifier))
        player.deck.shuffle()
        player.energy = 0

    def upgrade(self):
        super().upgrade()
        self.x_modifier = 1
