
class PlayerController:

    def __init__(self):
        pass

    def reset(self):
        pass

    def get_target(self, player, enemies, playable, debug):
        pass

    def get_scry(self, player, enemies, cards, debug):
        pass

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        self.counter += 1
        if self.delay != 0 and self.counter % (self.delay * self.framerate) != 0:
            return None, None
        self.counter = 0
        return None, True

    def handle_event(self, pos, player, clickables):
        pass

    def handle_map_event(self, pos, player, map_gen, cur_floor, avail_floors):
        pass

    def end_combat(self, player, enemies, debug):
        pass

    def begin_combat(self, player, enemies, debug):
        pass