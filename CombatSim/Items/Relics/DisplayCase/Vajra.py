from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

class Vajra(Relic):
    # At the start of each combat, gain 1 Strength.
    STRENGTH_AMOUNT = 1
    def __init__(self, player):
        super().__init__("Vajra", "Common", player)

        self.listener = Listener(Listener.Event.START_COMBAT, self.start_combat)
        self.end_combat_listener = Listener(Listener.Event.END_COMBAT, self.end_combat_listener)

    def start_combat(self, player, enemy, enemies, debug):
        self.player.damage_dealt_modifier += self.STRENGTH_AMOUNT

    def end_combat_listener(self, player, enemy, enemies, debug):
        self.player.damage_dealt_modifier -= self.STRENGTH_AMOUNT

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.end_combat_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.end_combat_listener)