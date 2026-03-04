from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption


_BASIC_CARD_NAMES = {"Strike", "Defend"}


def _is_basic(card) -> bool:
    return card.name in _BASIC_CARD_NAMES


class BonfireSpirits(Event):
    title = "Bonfire Spirits"
    description = (
        "You happen upon what looks like a group of purple fire spirits dancing "
        "around a large bonfire. The spirits toss small bones and fragments into "
        "the fire, which brilliantly erupts each time. As you approach, the "
        "spirits all turn to you, expectantly..."
    )

    def build_options(self):
        return [
            EventOption("Offer", "Offer a card to the spirits.", self.offer),
        ]

    def offer(self, player):
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
        rarity = self._rarity(card)
        player.deck.remove_card(card)
        self._apply_reward(player, rarity)

    def leave(self, player):
        pass

    # ------------------------------------------------------------------ #

    @staticmethod
    def _rarity(card) -> str:
        """
        Return the rarity of a card as a string.
        Currently inferred from card name; extend this when a rarity field is
        added to Card.
        """
        if _is_basic(card):
            return "Basic"
        if card.is_curse():
            return "Curse"
        # Fallback — treat unknown cards as Common until rarity is tracked.
        return "Common"

    @staticmethod
    def _apply_reward(player, rarity: str):
        if rarity == "Basic":
            pass  # Spirits ignore you; card removal is the only benefit.
        elif rarity == "Common":
            player.heal(5)
        elif rarity == "Uncommon":
            player.heal(player.start_health)
        elif rarity == "Rare":
            player.add_max_hp(10)
            player.heal(player.start_health)
        elif rarity == "Curse":
            player.add_card("SpiritPoop")  # TODO: implement Spirit Poop curse card
