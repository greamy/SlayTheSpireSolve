from CombatSim.Entities.Entity import Entity
from CombatSim.Entities.Status.Status import Status
from CombatSim.Actions.Listener import Listener


class Thorns(Status):
    ID = 6

    def __init__(self, duration: int, entity: Entity):
        self.id = self.ID

        self.entity = entity
        self.thorns_dmg = duration
        self.removed = False
        super().__init__(duration, entity, Listener(Listener.Event.IS_ATTACKED, self.on_attack))

    def on_attack(self, player, enemy, enemies, debug):
        lost_health = enemy.take_damage(self.thorns_dmg)
        if lost_health:
            player.notify_listeners(Listener.Event.TAKEN_DAMAGE, player, enemies, debug)
