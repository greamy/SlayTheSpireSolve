from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status import Status


class Vulnerable(Status):

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity)
        self.apply()

    def apply(self):
        self.entity.damage_taken_multiplier *= 1.5

    def remove(self):
        self.entity.damage_taken_multiplier /= 1.5
