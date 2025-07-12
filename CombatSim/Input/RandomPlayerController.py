import random

from CombatSim.Input.Controller import PlayerController


class RandomPlayerController(PlayerController):

    def __init__(self):
        super().__init__()

    def get_target(self, player, enemies, playable, debug):
        index = random.randint(0, len(enemies) - 1)
        return index, enemies[index]

    def get_scry(self, player, enemies, card, debug):
        choice = random.randint(0, 1)
        return choice and 1

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        if len(player.deck.hand) == 0:
            return None

        index = random.randint(0, len(playable_cards) - 1)
        card = playable_cards[index]
        i = player.deck.hand.index(card)

        if len(enemies) == 0:
            return card

        return i, card
