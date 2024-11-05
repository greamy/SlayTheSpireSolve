from CombatSim.Entities.Entity import Entity
from SpireBot.Environments.States.State import State


class EntityState(State):
    MAX_STATUS_ENCODING = 10

    def __init__(self, entity: Entity):
        self.entity = entity

    def get_state(self):
        pass