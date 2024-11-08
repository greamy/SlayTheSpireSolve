from CombatSim.Actions.Library.Insight import Insight
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Pray(Card):
    def __init__(self, player: Player):
        super().__init__("Pray", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None, id=54)
        self.mantra = 3
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        player.add_mantra(self.mantra)
        player.deck.draw_pile.append(Insight(player))
        player.deck.shuffle()
        # Gain 3(4) {{Mantra}}. Shuffle an {{C|Insight}} into your draw pile.

    def upgrade(self):
        super().upgrade()
        self.mantra = 4
