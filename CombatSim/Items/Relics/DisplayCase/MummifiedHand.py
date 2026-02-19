import random

from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class MummifiedHand(Relic):
    # Whenever you play a Power, a random card in your hand costs 0 for the turn.
    DAMAGE_AMOUNT = 3

    def __init__(self, player):
        super().__init__("Mummified Hand", "Common", player)
        self.power_listener = Listener(Listener.Event.POWER_PLAYED, self.on_power_played)
        self.end_turn_listener = Listener(Listener.Event.END_TURN, self.on_end_turn)
        self.cards_modified: {Card : int} = {}
        self.card_cost = None

    def on_power_played(self, player, enemy, enemies, debug):
        hand_without_zero_cost = [card for card in player.deck.hand if card.energy != 0]
        choice = random.choice(hand_without_zero_cost)
        self.cards_modified[choice] = choice.energy
        choice.energy = 0

    def on_end_turn(self, player, enemy, enemies, debug):
        for card in self.cards_modified:
            card.energy = self.cards_modified[card]
        self.cards_modified = {}

    def on_pickup(self):
        self.player.add_listener(self.power_listener)
        self.player.add_listener(self.end_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.power_listener)
        self.player.add_listener(self.end_turn_listener)

