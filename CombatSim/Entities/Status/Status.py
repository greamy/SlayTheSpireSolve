
class Status:
    NUM_STATUSES = 6
    def __init__(self, duration, entity):
        self.duration = duration
        self.entity = entity
        self.id = -1

    def decrement(self, player, enemy, enemies, debug):
        self.duration -= 1
        if self.duration == 0:
            self.remove()
            self.entity.status_list.remove(self)

    def apply(self):
        self.entity.status_list.append(self.id)

    def remove(self):
        pass
