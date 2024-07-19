from Entity import Entity


class Enemy(Entity):

    def __init__(self, health, block, status_list, intent, intent_set):
        super().__init__(health, block, status_list)
        self.intent = intent
        self.intent_set = intent_set


