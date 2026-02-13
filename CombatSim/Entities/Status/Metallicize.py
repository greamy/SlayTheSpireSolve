from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status
from CombatSim.Actions.Listener import Listener


class Metallicize(Status):
    ID = 4
    def __init__(self, duration, entity: Entity):
        self.id = 4

        self.entity = entity
        super().__init__(duration, entity, Listener(Listener.Event.END_TURN, self.do_block))

    def do_block(self, player, enemy, enemies, debug):
        self.entity.gain_block(self.duration, enemies, debug)
