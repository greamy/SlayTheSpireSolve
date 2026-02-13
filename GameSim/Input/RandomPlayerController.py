import random
import time
import numpy as np

from GameSim.Input.Controller import PlayerController


class RandomPlayerController(PlayerController):

    def __init__(self, delay=0):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60

    def get_target(self, player, enemies, playable, debug):

        self.counter = 0
        index = random.randint(0, len(enemies) - 1)
        return index, enemies[index]

    def get_scry(self, player, enemies, cards, debug):
        if not self.wait_for_counter():
            return None, None
        # list of length cards of boolean values
        to_discard = set()

        for i in range(random.randint(0,len(cards))):
            choice = random.randint(0,len(cards)-1)
            to_discard.add(choice)
        to_discard = list(to_discard)
        return to_discard

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        if not self.wait_for_counter():
            return None, None
        if len(player.deck.hand) == 0:
            return None, None

        index = random.randint(0, len(playable_cards) - 1)
        card = playable_cards[index]
        i = player.deck.hand.index(card)

        if len(enemies) == 0:
            return 0, card

        return i, card

    def get_map_choice(self, player, map_gen, floor, room_idx):
        if not self.wait_for_counter():
            return None
        avail_rooms = map_gen.get_avail_floors(floor, room_idx)
        return map_gen.map[floor][random.choice(avail_rooms)]

    def select_cards_from_zone(self, player, zone, enemies, num_cards, debug):
        card_choices = player.deck.get_zone(zone)
        num_available = len(card_choices)

        # Safety check: don't try to pick more cards than exist
        count_to_pick = min(num_cards, num_available)

        if count_to_pick == 0:
            return []

        # Generate random indices from 0 to length of card_choices
        # replace=False ensures we don't pick the same card twice
        selected_indices = np.random.choice(
            num_available,
            size=count_to_pick,
            replace=False
        )

        # np.random.choice returns a numpy array, so we convert to list
        return selected_indices.tolist()
        

