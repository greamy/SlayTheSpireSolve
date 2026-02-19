
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class GremlinHorn(Relic):
    # Whenever an enemy dies, gain 1 Energy and draw 1 card.

    def __init__(self, player):
        super().__init__("Gremlin Horn", "Common", player)
        self.listener = Listener(Listener.Event.ENEMY_DIED, self.on_enemy_die)

    def on_enemy_die(self, player, enemy, enemies, debug):
        self.player.energy += 1
        self.player.draw_cards(1, enemies, debug)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
