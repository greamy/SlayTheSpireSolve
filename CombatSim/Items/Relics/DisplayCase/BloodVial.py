from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class BloodVial(Relic):
    # At the start of each combat, heal 2 HP.
    def __init__(self, player):
        super().__init__("Blood Vial", "Common", player)
        self.listener = Listener(Listener.Event.START_COMBAT, self.start_combat)

    def start_combat(self, player, enemy, enemies, debug):
        self.player.heal(2)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)