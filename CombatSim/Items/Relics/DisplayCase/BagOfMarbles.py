from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

class BagOfMarbles(Relic):
    # At the start of each combat, apply 1  Vulnerable to ALL enemies.
    def __init__(self, player):
        super().__init__("Bag Of Marbles", "Common", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.start_combat)

    def start_combat(self, player, enemy, enemies, debug):
        for e in enemies:
            vuln = Vulnerable(1, e)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
