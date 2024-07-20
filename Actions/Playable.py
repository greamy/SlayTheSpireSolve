from Entities import Entity


class Playable:
    def __init__(self, damage, attacks, block, status):
        self.damage = damage
        self.attacks = attacks
        self.block = block
        self.status = status

    def play(self, primary_entity: Entity, target_entity: Entity, debug: bool):
        one_attack_damage = round((self.damage + primary_entity.damage_dealt_modifier) * primary_entity.damage_dealt_multiplier)
        target_entity.take_damage(one_attack_damage * self.attacks)
        primary_entity.block += self.block
        # TODO: Implement status effects

    def __str__(self):
        return ("Damage: " + str(self.damage) + " Attacks: " + str(self.attacks) +
                " Block: " + str(self.block) + " Status: " + str(self.status))