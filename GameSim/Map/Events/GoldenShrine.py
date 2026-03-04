from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption


class GoldenShrine(Event):
    title = "Golden Shrine"
    description = (
        "Before you lies an elaborate shrine to an ancient spirit."
    )

    def __init__(self, player, act, ascension):
        super().__init__(player, act, ascension)
        self.pray_gold_gain = 100
        if ascension > 15:
            self.pray_gold_gain = 50

    def build_options(self):
        return [
            EventOption("Pray", "Gain 100 (50) Gold.", self.pray),
            EventOption("Desecrate", "Gain 275 Gold. Become Cursed - Regret.", self.desecrate),
            EventOption("Leave", ""),
        ]

    def pray(self, player):
        player.gain_gold(self.pray_gold_gain, [], False)

    def desecrate(self, player):
        player.gain_gold(275, [], False)
        player.add_card("Regret")

    def leave(self, player):
        pass
