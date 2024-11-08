from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status


class Weak(Status):
    ID = 1
    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)
        self.id = 1
        self.apply()

    def apply(self):
        super().apply()
        self.entity.damage_dealt_multiplier *= 0.75

    def remove(self):
        self.entity.damage_dealt_multiplier /= 0.75
