from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status


class Frail(Status):
    ID = 3
    BLOCK_MULTIPLIER = 0.75

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity, Listener(Listener.Event.START_TURN, self.decrement, duration))
        self.apply()

    def apply(self):
        if super().apply():
            self.entity.block_multiplier *= self.BLOCK_MULTIPLIER

    def remove(self):
        self.entity.block_multiplier /= self.BLOCK_MULTIPLIER
