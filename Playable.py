
class Playable:
    def __init__(self, damage, attacks, block, status):
        self.damage = damage
        self.attacks = attacks
        self.block = block
        self.status = status

    def play(self, primary_entity, target_entity):
        target_entity.take_damage(self.damage * self.attacks)
        primary_entity.block += self.block
        # TODO: Implement status effects