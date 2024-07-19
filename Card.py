
class Card:
    def __init__(self, name, energy, damage, attacks, block, types, exhaust, status):
        self.name = name
        self.energy = energy
        self.damage = damage
        self.attacks = attacks
        self.block = block
        self.types = types
        self.exhaust = exhaust
        self.status = status



    def __str__(self):
        return self.name