
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class RegalPillow(Relic):
    # Heal an additional 15 HP when you Rest.
    HEAL_AMOUNT = 15
    def __init__(self, player):
        super().__init__("Regal Pillow", "Common", player)
        self.listener = Listener(Listener.Event.REST_SITE, self.on_rest_site)

    def on_rest_site(self, player, enemy, enemies, debug):
        player.heal(15)


    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)