from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
import random


class Meditate(Card):
    def __init__(self, player: Player):
        super().__init__("Meditate", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, Player.Stance.CALM)
        self.num_cards = 1
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_retain)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
        for i in range(self.num_cards):
            card = random.choice(player.deck.discard_pile)
            player.deck.hand.append(card)
            player.deck.discard_pile.remove(card)
            card.temp_retain = True
        player.turn_over = True

    def do_retain(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            card.temp_retain = False
        player.listeners.remove(self.listener)

    def upgrade(self):
        super().upgrade()
        self.num_cards = 2
