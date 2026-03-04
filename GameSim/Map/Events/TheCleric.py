from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

_HEAL_COST = 35
_PURIFY_COST = 50
_PURIFY_COST_HIGH_ASCENSION = 75
_HIGH_ASCENSION = 15


class TheCleric(Event):
    title = "The Cleric"
    description = (
        "You come across a wandering priest. He smiles warmly. "
        "'I can offer healing or remove a troublesome card, for a price.'"
    )

    def build_options(self):
        purify_cost = _PURIFY_COST_HIGH_ASCENSION if self.ascension >= _HIGH_ASCENSION else _PURIFY_COST
        options = []
        if self.player.gold >= _HEAL_COST:
            options.append(EventOption(
                f"Heal ({_HEAL_COST} gold)",
                "Heal 25% of your max HP.",
                self.heal,
            ))
        if self.player.gold >= purify_cost:
            options.append(EventOption(
                f"Purify ({purify_cost} gold)",
                "Remove a card from your deck.",
                self.purify,
            ))
        options.append(EventOption("Leave", ""))
        return options

    def heal(self, player):
        player.gold -= _HEAL_COST
        player.heal(player.start_health // 4)

    def purify(self, player):
        purify_cost = _PURIFY_COST_HIGH_ASCENSION if self.ascension >= _HIGH_ASCENSION else _PURIFY_COST
        chosen = player.controller.select_cards_from_zone(
            player,
            Player.Deck.Zone.DRAW_PILE,
            [],
            1,
            False,
        )
        if not chosen:
            return
        card = player.deck.draw_pile[chosen[0]]
        player.deck.remove_card(card)
        player.gold -= purify_cost

    def leave(self, player):
        pass