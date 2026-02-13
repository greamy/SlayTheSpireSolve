
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class JuzuBracelet(Relic):
    # Regular enemy combats are no longer encountered in ? rooms.
    def __init__(self, player):
        super().__init__("Juzu Bracelet", "Common", player)

    # def on_rest_site(self, player, enemy, enemies, debug):
    #     self.has_rested = True
    #
    # def on_begin_combat(self, player, enemy, enemies, debug):
    #     if self.has_rested:
    #         player.energy += 2
    #         self.has_rested = False

    def on_pickup(self):
        # self.player.add_listener(self.listener)
        pass

    def on_drop(self):
        # self.player.remove_listener(self.listener)
        pass
