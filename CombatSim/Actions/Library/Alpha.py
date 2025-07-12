from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Beta import Beta
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player


class Alpha(Card):
    def __init__(self, player: Player):
        super().__init__("Alpha", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, False, player, None, id=0)
        self.description = "Shuffle a Beta into your draw pile. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, enemy, enemies, debug)
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        player.deck.draw_pile.append(Beta(player))
        player.deck.shuffle()

    def upgrade(self):
        super().upgrade()
        self.description = "Innate. " + self.description
        self.innate = True

