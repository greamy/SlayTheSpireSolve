from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic


class BottledFlame(Relic):
    # Upon pick up, choose an Attack. Start each combat with this card in your hand.
    def __init__(self, player):
        super().__init__("Blue Candle", "Common", player)


    def on_pickup(self):
        self.player.deck.reshuffle()
        # TODO: Make sure this only chooses attacks
        card_idx = self.player.controller.select_cards_from_zone(self.player, Player.Deck.Zone.DRAW_PILE, [], 1, False)[0]
        self.player.deck.draw_pile[card_idx].innate = True

    def on_drop(self):
        pass
