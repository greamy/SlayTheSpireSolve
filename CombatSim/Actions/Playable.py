from CombatSim.Actions.Listener import Listener
from CombatSim.Entities import Entity


class Playable:
    def __init__(self, damage, attacks, block):
        self.damage = damage
        self.attacks = attacks
        self.block = block
        self.one_attack_damage = 0

    def play(self, primary_entity: Entity, primary_list: list[Entity], target_entity: Entity, target_list: list[Entity], debug: bool):
        self.get_damage(primary_entity, target_entity)
        for i in range(self.attacks):
            target_entity.take_damage(self.one_attack_damage)
            target_entity.notify_listeners(Listener.Event.TAKEN_DAMAGE, primary_entity, [target_entity], debug)
        primary_entity.gain_block(self.block, target_list, debug)

    def get_damage(self, primary_entity: Entity, target_entity: Entity):
        self.one_attack_damage = round((self.damage + primary_entity.damage_dealt_modifier) * primary_entity.damage_dealt_multiplier)
        return self.one_attack_damage * self.attacks * target_entity.damage_taken_multiplier

    def __str__(self):
        return ("Damage: " + str(self.damage) + " Attacks: " + str(self.attacks) +
                " Block: " + str(self.block))
