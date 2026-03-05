from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption



class TheDuplicator(Event):
    title = "The Duplicator"
    description = (
        "Before you lies a decorated altar to some ancient entity."
    )

    def build_options(self):
        return [
            EventOption("Pray", "Duplicate a card in your deck.", self.pray),
            EventOption("Leave", ""),
        ]

    def pray(self, player):
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
        # create new card that is the same card subclass:
        duplicated = card.__class__(player)
        player.deck.draw_pile.append(duplicated)

    def leave(self, player):
        pass
