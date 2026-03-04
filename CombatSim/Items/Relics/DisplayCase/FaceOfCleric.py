from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic


class FaceOfCleric(Relic):
    # After each combat, gain 1 Max HP.
    def __init__(self, player):
        super().__init__("FaceOfCleric", "Event", player)
        self.listener = Listener(Listener.Event.END_COMBAT, self.gain_max_hp)

    def gain_max_hp(self, player, enemy, enemies, debug):
        self.player.add_max_hp(1)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)
