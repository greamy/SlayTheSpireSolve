from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status
from CombatSim.Actions.Listener import Listener


class PlatedArmor(Status):
    ID = 5
    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)
        self.listener = Listener(Listener.Event.TAKEN_DAMAGE, self.decrement)
        entity.add_listener(self.listener)

        self.block_listener = Listener(Listener.Event.END_TURN, self.do_block)
        entity.add_listener(self.block_listener)

    def do_block(self, player, enemy, enemies, debug):
        player.gain_block(self.duration, enemies, debug)

    def apply(self):
        super().apply()

    def remove(self):
        self.entity.listeners.remove(self.block_listener)
