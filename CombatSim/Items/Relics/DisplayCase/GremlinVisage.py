from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Weak import Weak
from CombatSim.Items.Relics.Relic import Relic


class GremlinVisage(Relic):
    # Start each combat with 1 Weak.
    def __init__(self, player):
        super().__init__("GremlinVisage", "Event", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.apply_weak)

    def apply_weak(self, player, enemy, enemies, debug):
        Weak(1, self.player)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)