from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class Meditate(Card):
    def __init__(self, player: Player):
        super().__init__("Meditate", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, Player.Stance.CALM)
        self.num_cards = 1
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_retain)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
        if self.num_cards > len(player.deck.discard_pile):
            num_cards = len(player.deck.discard_pile)
        else:
            num_cards = self.num_cards
        for i in range(num_cards):
            card = random.choice(player.deck.discard_pile)
            player.deck.hand.append(card)
            player.deck.discard_pile.remove(card)
            card.temp_retain = True
            player.notify_listeners(Listener.Event.HAND_CHANGED, enemies, debug)
        player.turn_over = True

    def do_retain(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            card.temp_retain = False
        player.listeners.remove(self.listener)

    def upgrade(self):
        super().upgrade()
        self.num_cards = 2
