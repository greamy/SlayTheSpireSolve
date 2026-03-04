from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.WarpedTongs import WarpedTongs
from GameSim.Map.Event import Event, EventOption


class OminousForge(Event):
    title = "Ominous Forge"
    description = (
        "You duck into a small hut. Inside, you find what appears to be a forge. "
        "The smithing tools are covered with dust, yet a fire roars inside the furnace. You feel on edge..."
    )

    def __init__(self, player, act, ascension):
        super().__init__(player, act, ascension)
        self.pray_gold_gain = 100
        if ascension > 15:
            self.pray_gold_gain = 50

    def build_options(self):
        return [
            EventOption("Forge", "Upgrade a card.", self.forge),
            EventOption("Rummage", "Obtain Warped Tongs. Become Cursed - Pain.", self.rummage),
            EventOption("Leave", ""),
        ]

    def forge(self, player):
        chosen = player.controller.select_cards_from_zone(
            player,
            Player.Deck.Zone.DRAW_PILE,
            [],
            1,
            False,
            lambda c: not c.upgraded
        )
        if not chosen:
            return

        player.deck.draw_pile[chosen[0]].upgrade()

    def rummage(self, player):
        tongs = WarpedTongs(player)
        player.add_relic(tongs)
        player.add_card("Pain")

    def leave(self, player):
        pass
