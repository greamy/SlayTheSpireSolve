
class Status:
    def __init__(self, duration, entity):
        self.duration = duration
        self.entity = entity

    def decrement(self, player, enemy, enemies, debug):
        self.duration -= 1
        if self.duration == 0:
            self.remove()

    def apply(self):
        pass

    def remove(self):
        pass
