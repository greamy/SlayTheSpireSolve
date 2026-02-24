from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic


class BottledTornado(Relic):
    # Upon pick up, choose a Power. Start each combat with this card in your hand.
    def __init__(self, player):
        super().__init__("Bottled Tornado", "Common", player)


    def on_pickup(self):
        self.player.deck.reshuffle()
        chosen_idxs = self.player.controller.select_cards_from_zone(player=self.player, zone=Player.Deck.Zone.DRAW_PILE,
                                                                 enemies=[], num_cards=1, debug=False,
                                                                 condition=self.is_valid_card)
        if chosen_idxs is None:
            return
        card_idx = chosen_idxs[0]
        self.player.deck.draw_pile[card_idx].innate = True

    def is_valid_card(self, card: Card):
        return card.card_type == Card.Type.POWER

    def on_drop(self):
        pass
