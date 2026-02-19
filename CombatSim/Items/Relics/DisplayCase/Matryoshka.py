
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Matryoshka(Relic):
    # The next 2 chests you open contain 2 Relics. (Excludes boss chests)
    def __init__(self, player):
        super().__init__("Matryoshka", "Common", player)

    # def on_rest_site(self, player, enemy, enemies, debug):
    #     self.has_rested = True
    #

    def on_pickup(self):
        # self.player.add_listener(self.listener)
        pass

    def on_drop(self):
        # self.player.remove_listener(self.listener)
        pass
