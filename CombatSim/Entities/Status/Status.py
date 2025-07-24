
class Status:
    NUM_STATUSES = 6
    ID = -1

    def __init__(self, duration, entity):
        self.duration = duration
        self.entity = entity
        self.listener = None

    def decrement(self, player, enemy, enemies, debug):
        self.duration -= 1
        if self.duration == 0:
            self.remove()
            self.entity.status_list.remove(self.ID)

    def apply(self):
        self.entity.status_list.append(self.ID)

    def remove(self):
        pass

    def remove_listener(self):
        if self.listener is not None:
            self.entity.remove_listener(self.listener)
            # self.listener = None

