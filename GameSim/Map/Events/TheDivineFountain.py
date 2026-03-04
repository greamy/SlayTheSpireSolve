from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption



class TheDivineFountain(Event):
    title = "The Divine Fountain"
    description = (
        "You come across shimmering water flowing endlessly from a fountain on a nearby wall. "
    )

    def build_options(self):
        return [
            EventOption("Drink", "Remove all Curses from your deck.", self.drink),
            EventOption("Leave", ""),
        ]

    def drink(self, player):
        for card in player.deck:
            if card.is_curse():
                player.deck.remove_card(card)

    def leave(self, player):
        pass