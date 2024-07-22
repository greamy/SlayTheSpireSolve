class Entity:

    def __init__(self, health, status_list):
        self.health = health
        self.block = 0
        self.status_list = status_list
        self.damage_dealt_multiplier = 1.0
        self.damage_dealt_modifier = 0
        self.damage_taken_multiplier = 1.0

    def do_turn(self, opponents, debug):
        pass

    def start_turn(self, opponents, debug):
        # TODO: Decrement all timed statuses by one
        self.block = 0

    def take_damage(self, amount):
        if self.block > 0:
            self.block -= round(amount*self.damage_taken_multiplier)
            if self.block < 0:
                self.health -= abs(self.block)
                self.block = 0
        else:
            self.health -= round(amount*self.damage_dealt_multiplier)

        if self.health <= 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def gain_status(self, status):
        self.status_list.append(status)

    def lose_status(self, status):
        self.status_list.remove(status)


