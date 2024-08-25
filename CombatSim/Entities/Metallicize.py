from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status import Status
from CombatSim.Actions.Listener import Listener


class Metallicize(Status):

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)

        self.block_listener = Listener(Listener.Event.END_TURN, self.do_block)
        entity.add_listener(self.block_listener)

    def do_block(self, player, enemy, enemies, debug):
        player.gain_block(self.duration, enemies, debug)

    def apply(self):
        pass

    def remove(self):
        pass
