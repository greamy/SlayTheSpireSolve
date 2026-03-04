import random

from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

_BASIC_CARD_NAMES = {"Strike", "Defend"}
_STARTER_CARDS = {"Eruption", "Vigilance"}

class Transmogrifier(Event):
    title = "Transmogrifier"
    description = (
        "Before you lies an elaborate shrine to a forgotten spirit."
    )

    def build_options(self):
        return [
            EventOption("Pray", "Transform a card.", self.pray),
            EventOption("Leave", "")
        ]

    def pray(self, player):
        chosen = player.controller.select_cards_from_zone(
            player,
            Player.Deck.Zone.DRAW_PILE,
            [],
            1,
            False,
            lambda c: c.name in _BASIC_CARD_NAMES or c.is_curse()
        )
        if not chosen:
            return

        card = player.deck.draw_pile[chosen[0]]
        player.deck.remove_card(card)

        # Build valid targets: instantiate each card temporarily (no side effects)
        # to check its type, then discard the instance.
        transform_options = []
        for name, module in player.implemented_cards.items():
            NON_TRANSFORMABLE_CARDS = ["Miracle", "Expunger"]
            if name in _BASIC_CARD_NAMES or name in _STARTER_CARDS or name in NON_TRANSFORMABLE_CARDS:
                continue
            cls = getattr(module, name)
            test = cls(player)
            if not test.is_curse() and not test.card_type.value == 3:  # exclude STATUS
                transform_options.append(name)

        if not transform_options:
            return

        transform_name = random.choice(transform_options)
        player.add_card(transform_name)

    def leave(self, player):
        pass
