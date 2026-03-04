from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

_BASIC_CARD_NAMES = {"Strike", "Defend"}


def _is_basic(card) -> bool:
    return card.name in _BASIC_CARD_NAMES

class Purifier(Event):
    title = "Purifier"
    description = (
        "Before you lies an elaborate shrine to a forgotten spirit."
    )

    def build_options(self):
        return [
            EventOption("Pray", "Remove a card from your deck.", self.pray),
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

    def leave(self, player):
        pass
