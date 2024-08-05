from Entities.Entity import Entity
from Entities.Status import Status


class Weak(Status):

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)
        self.apply()

    def apply(self):
        self.entity.damage_dealt_multiplier *= 0.75

    def remove(self):
        self.entity.damage_dealt_multiplier /= 0.75
