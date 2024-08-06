from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Actions.Library.Insight import Insight


class Study(Card):
    def __init__(self, player: Player):
        super().__init__("Study", Card.Type.POWER, 2, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener(Listener.Event.END_TURN, self.do_power)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # At the end of your turn, shuffle an {{C|Insight}} into your draw pile.
        super().play(player, target_enemy, enemies, debug)
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        player.deck.draw_pile.append(Insight(player))
        player.deck.shuffle()

    def upgrade(self):
        super().upgrade()
        self.energy = 1
