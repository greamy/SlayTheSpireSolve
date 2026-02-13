from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status


class Vulnerable(Status):
    ID = 0
    DAMAGE_TAKEN_MULTIPLIER = 1.5

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity, Listener(Listener.Event.START_TURN, self.decrement, duration))

    def apply(self):
        if super().apply():
            self.entity.damage_taken_multiplier *= self.DAMAGE_TAKEN_MULTIPLIER

    def remove(self):
        self.entity.damage_taken_multiplier /= self.DAMAGE_TAKEN_MULTIPLIER
