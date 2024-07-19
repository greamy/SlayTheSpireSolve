
class Entity:

    def __init__(self, health, block, status_list):
        self.health = health
        self.block = block
        self.status_list = status_list

    def take_damage(self, amount):
        if self.block > 0:
            self.block -= amount
            if self.block < 0:
                self.health -= abs(self.block)
            self.block = 0
        else:
            self.health -= amount

    def gain_status(self, status):
        self.status_list.append(status)

    def lose_status(self, status):
        self.status_list.remove(status)


