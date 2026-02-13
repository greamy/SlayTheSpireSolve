from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status
from CombatSim.Actions.Listener import Listener


class Metallicize(Status):
    ID = 4
    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity, Listener(Listener.Event.END_TURN, self.do_block))
        self.id = 4

        self.entity = entity
        self.removed = False

    def do_block(self, player, enemy, enemies, debug):
        self.entity.gain_block(self.duration, enemies, debug)

    def remove(self):
        if not self.removed:
            self.entity.listeners.remove(self.block_listener)
            self.removed = True

    def remove_listeners(self):
        self.entity.remove_listener(self.block_listener)
        # super().remove_listeners()
