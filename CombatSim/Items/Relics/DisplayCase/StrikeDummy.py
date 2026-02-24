from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class StrikeDummy(Relic):
    # Cards containing "Strike" deal 3 additional damage.
    DAMAGE_INCREASE = 3

    def __init__(self, player):
        super().__init__("Strike Dummy", "Uncommon", player)
        self.listener = Listener(Listener.Event.CARD_ADDED_TO_DECK, self.on_card_add)
        self.cards_with_strike = []

    def _set_strike_cards(self, player):
        new_strike_cards = [card for card in player.deck if
                            card not in self.cards_with_strike
                            and "strike" in card.name.lower()]
        for strike in new_strike_cards:
            strike.damage += self.DAMAGE_INCREASE
        self.cards_with_strike.extend(new_strike_cards)

    def on_card_add(self, player, enemy, enemies, debug):
        self._set_strike_cards(player)

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.cards_with_strike = [card for card in self.player.deck if "strike" in card.name.lower()]
        for strike in self.cards_with_strike:
            strike.damage += self.DAMAGE_INCREASE

    def on_drop(self):
        pass
