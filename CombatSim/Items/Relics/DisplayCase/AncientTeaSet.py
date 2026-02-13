
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class AncientTeaSet(Relic):
    # Whenever you enter a Rest Site, start the next combat with 2 extra Energy.
    ENERGY_AMOUNT = 2
    def __init__(self, player):
        super().__init__("Ancient Tea Set", "Common", player)
        self.listener = Listener(Listener.Event.REST_SITE, self.on_rest_site)
        self.begin_combat_listener = Listener(Listener.Event.START_COMBAT, self.on_begin_combat)
        self.has_rested = False

    def on_rest_site(self, player, enemy, enemies, debug):
        self.has_rested = True

    def on_begin_combat(self, player, enemy, enemies, debug):
        if self.has_rested:
            player.energy += 2
            self.has_rested = False

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.begin_combat_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.begin_combat_listener)
