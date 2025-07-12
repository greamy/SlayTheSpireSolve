from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Expunger import Expunger


class ConjureBlade(Card):
    def __init__(self, player: Player):
        super().__init__("ConjureBlade", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, player, None, id=11)
        self.description = "Shuffle an Expunger with X into your draw pile. Exhaust."
        self.x_modifier = 0

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Shuffle an {{C|Expunger}} with X(+1) into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Expunger(player, player.energy + self.x_modifier))
        player.deck.shuffle()
        player.energy = 0

    def upgrade(self):
        super().upgrade()
        self.description = "Shuffle an Expunger with X+1 into your draw pile. Exhaust."
        self.x_modifier = 1
