from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

class BagOfPreparation(Relic):
    # At the start of each combat, draw 2 additional cards.
    DRAW_AMT = 2
    def __init__(self, player):
        super().__init__("Bag Of Preparation", "Common", player)

        self.listener = Listener(Listener.Event.START_COMBAT, self.start_combat)

    def start_combat(self, player, enemy, enemies, debug):
        self.player.draw_cards(self.DRAW_AMT, enemies, debug)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)