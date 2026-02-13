from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class PotionBelt(Relic):
    # Upon pick up, gain 2 potion slots.
    def __init__(self, player):
        super().__init__("Potion Belt", "Common", player)

    def on_trigger(self, player, enemy, enemies, debug):
        pass

    def on_pickup(self):
        # TODO: Increase player potion slots by 2
        pass

    def on_drop(self):
        # TODO: Decrease player potion slots by 2
        pass
