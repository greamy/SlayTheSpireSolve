import random

from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption

_BASIC_CARD_NAMES = {"Strike", "Defend"}
_MIN_GOLD = 50
_MAX_GOLD = 150


class WeMeetAgain(Event):
    title = "We Meet Again!"
    description = (
        "An eccentrically dressed man runs up to you. 'We finally meet again! "
        "I have been waiting for you!' You have no recollection of this man..."
    )

    def build_options(self):
        options = [
            EventOption("Give Gold", f"Lose {_MIN_GOLD}-{_MAX_GOLD} gold. Obtain a relic.", self.give_gold),
            EventOption("Give Card", "Lose a non-basic, non-curse card. Obtain a relic.", self.give_card),
            EventOption("Attack", "Nothing happens.", self.attack),
        ]
        if self.player.potions:
            options.insert(0, EventOption("Give Potion", "Lose a potion. Obtain a relic.", self.give_potion))
        return options

    def give_potion(self, player):
        # TODO: implement potion selection and removal
        pass

    def give_gold(self, player):
        gold_cost = min(player.gold, random.randint(_MIN_GOLD, _MAX_GOLD))
        player.gold -= gold_cost
        self._give_random_relic(player)

    def give_card(self, player):
        chosen = player.controller.select_cards_from_zone(
            player,
            Player.Deck.Zone.DRAW_PILE,
            [],
            1,
            False,
            lambda c: c.name not in _BASIC_CARD_NAMES and not c.is_curse(),
        )
        if not chosen:
            return
        card = player.deck.draw_pile[chosen[0]]
        player.deck.remove_card(card)
        self._give_random_relic(player)

    def attack(self, player):
        pass

    @staticmethod
    def _give_random_relic(player):
        if not player.implemented_relics:
            return
        relic_name = random.choice(list(player.implemented_relics.keys()))
        cls = getattr(player.implemented_relics[relic_name], relic_name)
        player.add_relic(cls(player))
