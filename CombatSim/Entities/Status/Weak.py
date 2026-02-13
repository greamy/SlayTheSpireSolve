from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status


class Weak(Status):
    ID = 1
    DAMAGE_DEALT_MULTIPLIER = 0.75

    def __init__(self, duration, entity: Entity):
        super().__init__(duration, entity, Listener(Listener.Event.START_TURN, self.decrement, duration))
        self.id = 1
        self.apply()

    def apply(self):
        if super().apply():
            self.entity.damage_dealt_multiplier *= self.DAMAGE_DEALT_MULTIPLIER

    def remove(self):
        self.entity.damage_dealt_multiplier /= self.DAMAGE_DEALT_MULTIPLIER
