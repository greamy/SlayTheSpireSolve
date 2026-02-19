from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Pantograph(Relic):
    # At the start of boss combats, heal 25 HP.
    HEAL_AMOUNT = 25

    def __init__(self, player):
        super().__init__("Pantograph", "Uncommon", player)
        self.boss_listener = Listener(Listener.Event.BOSS_START, self.on_boss_start)

    def on_boss_start(self, player, enemy, enemies, debug):
        player.heal(self.HEAL_AMOUNT)

    def on_pickup(self):
        self.player.add_listener(self.boss_listener)

    def on_drop(self):
        self.player.remove_listener(self.boss_listener)
