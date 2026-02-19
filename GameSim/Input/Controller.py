
class PlayerController:

    def __init__(self):
        pass

    def reset(self):
        pass

    def wait_for_counter(self):
        self.counter += 1
        if self.delay != 0 and self.counter % (self.delay * self.framerate) != 0:
            return False
        self.counter = 0
        return True

    def get_target(self, player, enemies, playable, debug):
        pass

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        pass

    def get_map_choice(self, player, map_gen, floor, room_idx):
        pass

    def get_scry(self, player, enemies, cards, debug):
        pass

    def handle_event(self, pos, player, clickables):
        pass

    def handle_map_event(self, pos, player, map_gen, cur_floor, avail_floors):
        pass

    def start_turn(self, player, enemies):
        pass

    def end_combat(self, player, enemies, debug):
        pass

    def begin_combat(self, player, enemies, debug):
        pass

    def select_cards_from_zone(self, player, zone, enemies, num_cards, debug, condition=None):
        pass