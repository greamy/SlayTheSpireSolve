
class Status:
    NUM_STATUSES = 6
    ID = -1

    def __init__(self, duration, entity, listener=None):
        self.duration = duration
        self.entity = entity
        self.listener = listener

    def decrement(self, player, enemy, enemies, debug):
        self.duration -= 1
        if self.duration == 0:
            self.remove()
            self.entity.status_list.remove(self)

    def apply(self) -> bool:
        for status in self.entity.status_list:
            if self.ID == status.ID:
                status.duration += self.duration
                self.listener = None
                return False

        self.entity.status_list.append(self)
        if self.listener is not None:
            self.entity.add_listener(self.listener)
        return True

    def remove(self):
        if self.listener is not None:
            self.entity.remove_listener(self.listener)

    def remove_listener(self):
        if self.listener is not None:
            self.entity.remove_listener(self.listener)
            # self.listener = None

