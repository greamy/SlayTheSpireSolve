from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Sundial(Relic):
    # Every 3 times you shuffle your draw pile, gain 2 Energy.
    ENERGY_AMOUNT = 2

    def __init__(self, player):
        super().__init__("Sundial", "Uncommon", player)
        self.shuffle_listener = Listener(Listener.Event.SHUFFLE, self.on_shuffle)
        self.shuffle_count = 0

    def on_shuffle(self, player, enemy, enemies, debug):
        self.shuffle_count += 1
        if self.shuffle_count == 3:
            player.energy += self.ENERGY_AMOUNT
            self.shuffle_count = 0

    def on_pickup(self):
        self.player.add_listener(self.shuffle_listener)

    def on_drop(self):
        self.player.remove_listener(self.shuffle_listener)
