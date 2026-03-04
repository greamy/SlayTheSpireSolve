import random

from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

_BASIC_CARD_NAMES = {"Strike", "Defend"}
_STARTER_CARDS = {"Eruption", "Vigilance"}

class UpgradeShrine(Event):
    title = "Upgrade Shrine"
    description = (
        "Before you lies an elaborate shrine to a forgotten spirit."
    )

    def build_options(self):
        return [
            EventOption("Pray", "Upgrade a card", self.pray),
            EventOption("Leave", "", self.leave)
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
        card.upgrade()

    def leave(self, player):
        pass
