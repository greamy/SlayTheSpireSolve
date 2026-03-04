from CombatSim.Items.Relics.Relic import Relic

_GOLD_MULTIPLIER = 1.25


class GoldenIdol(Relic):
    # Gain 25% more Gold from combat.
    def __init__(self, player):
        super().__init__("GoldenIdol", "Special", player)

    def on_pickup(self):
        self.player.gold_combat_multiplier *= _GOLD_MULTIPLIER

    def on_drop(self):
        self.player.gold_combat_multiplier /= _GOLD_MULTIPLIER
