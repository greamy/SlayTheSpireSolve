from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class MeatOnTheBone(Relic):
    # If your HP is at or below 50% at the end of combat, heal 12 HP.
    HEAL_AMOUNT = 12

    def __init__(self, player):
        super().__init__("Meat on the Bone", "Common", player)
        self.end_combat_listener = Listener(Listener.Event.END_COMBAT, self.on_end_combat)
        self.attack_count = 0

    def on_end_combat(self, player, enemy, enemies, debug):
        if player.health <= player.start_health / 2:
            player.heal(self.HEAL_AMOUNT)

    def on_pickup(self):
        self.player.add_listener(self.end_combat_listener)

    def on_drop(self):
        self.player.remove_listener(self.end_combat_listener)

