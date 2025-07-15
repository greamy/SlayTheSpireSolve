import random

from GameSim.Input.Controller import PlayerController


class RandomPlayerController(PlayerController):

    def __init__(self):
        super().__init__()

    def get_target(self, player, enemies, playable, debug):
        index = random.randint(0, len(enemies) - 1)
        return index, enemies[index]

    def get_scry(self, player, enemies, cards, debug):
        # list of length cards of boolean values
        to_discard = set()

        for i in range(random.randint(0,len(cards))):
            choice = random.randint(0,len(cards)-1)
            to_discard.add(choice)
        to_discard = list(to_discard)
        return to_discard


    def get_card_to_play(self, player, enemies, playable_cards, debug):
        if len(player.deck.hand) == 0:
            return None

        index = random.randint(0, len(playable_cards) - 1)
        card = playable_cards[index]
        i = player.deck.hand.index(card)

        if len(enemies) == 0:
            return card

        return i, card
