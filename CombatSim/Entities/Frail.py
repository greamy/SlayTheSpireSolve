from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status import Status


class Frail(Status):

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)
        self.apply()

    def apply(self):
        self.entity.block_multiplier *= 0.75

    def remove(self):
        self.entity.block_multiplier /= 0.75
