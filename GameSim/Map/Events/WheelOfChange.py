import random

from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

# Gold awarded per act
_ACT_GOLD = {1: 100, 2: 200, 3: 300}
_DAMAGE_PERCENT = 0.10
_DAMAGE_PERCENT_HIGH_ASCENSION = 0.15
_HIGH_ASCENSION = 15

_OUTCOMES = [
    "gain_gold",
    "gain_relic",
    "heal_full",
    "curse_decay",
    "remove_card",
    "take_damage",
]


class WheelOfChange(Event):
    title = "Wheel of Change"
    description = (
        "A dapper looking, cheery gremlin stands before an elaborate wheel. "
        "'Step right up! Everyone's a winner!' He gives the wheel a spin..."
    )

    def build_options(self):
        return [
            EventOption("Spin", "Let fate decide.", self.spin),
        ]

    def spin(self, player):
        outcome = random.choice(_OUTCOMES)
        getattr(self, f"_outcome_{outcome}")(player)

    # ------------------------------------------------------------------ #
    # Outcomes                                                             #
    # ------------------------------------------------------------------ #

    def _outcome_gain_gold(self, player):
        gold = _ACT_GOLD.get(self.act, 100)
        player.gold += gold

    def _outcome_gain_relic(self, player):
        if not player.implemented_relics:
            return
        relic_name = random.choice(list(player.implemented_relics.keys()))
        cls = getattr(player.implemented_relics[relic_name], relic_name)
        player.add_relic(cls(player))

    def _outcome_heal_full(self, player):
        player.heal(player.start_health)

    def _outcome_curse_decay(self, player):
        player.add_card("Decay")

    def _outcome_remove_card(self, player):
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

    def _outcome_take_damage(self, player):
        pct = _DAMAGE_PERCENT_HIGH_ASCENSION if self.ascension >= _HIGH_ASCENSION else _DAMAGE_PERCENT
        player.take_damage(int(player.start_health * pct))
