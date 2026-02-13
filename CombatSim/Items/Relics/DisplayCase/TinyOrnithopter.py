from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class TinyOrnithopter(Relic):
    # Whenever you use a potion, heal 5 HP.
    def __init__(self, player):
        super().__init__("Tiny Ornithopter", "Common", player)

    def on_trigger(self, player, enemy, enemies, debug):
        pass

    def on_pickup(self):
        # self.player.add_listener(self.listener)
        pass

    def on_drop(self):
        # self.player.remove_listener(self.listener)
        pass
