from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class MercuryHourglass(Relic):
    # At the start of your turn, deal 3 damage to ALL enemies.
    DAMAGE_AMOUNT = 3

    def __init__(self, player):
        super().__init__("Mercury Hourglass", "Common", player)
        self.start_turn_listener = Listener(Listener.Event.START_TURN, self.on_start_turn)

    def on_start_turn(self, player, enemy, enemies, debug):
        for e in enemies:
            e.take_damage(self.DAMAGE_AMOUNT)

    def on_pickup(self):
        self.player.add_listener(self.start_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.start_turn_listener)

