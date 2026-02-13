from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class PreservedInsect(Relic):
    # Enemies in Elite rooms have 25% less HP.
    def __init__(self, player):
        super().__init__("Preserved Insect", "Common", player)
        self.listener = Listener(Listener.Event.ENTER_ELITE, self.on_enter_elite)

    def on_enter_elite(self, player, enemy, enemies, debug):
        for enemy in enemies:
            enemy.health = int(enemy.health * 0.75)

    def on_pickup(self):
        self.player.add_listener(self.listener)
        pass

    def on_drop(self):
        self.player.remove_listener(self.listener)
