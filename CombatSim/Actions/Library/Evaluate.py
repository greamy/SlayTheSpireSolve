from CombatSim.Actions.Library.Insight import Insight
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Evaluate(Card):
    def __init__(self, player: Player):
        super().__init__("Evaluate", Card.Type.SKILL, 1, 0, 0, 6, 0, 0, False, False, player, None, id=29)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.deck.draw_pile.append(Insight(player))
        player.deck.shuffle()
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.

    def upgrade(self):
        super().upgrade()
        self.block = 10
