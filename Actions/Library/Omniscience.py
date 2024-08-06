from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
import random


class Omniscience(Card):
    def __init__(self, player: Player):
        super().__init__("Omniscience", Card.Type.SKILL, 4, 0, 0, 0, 0, 0, True, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. {{Exhaust}}.
        # TODO: make not random
        if len(player.deck.draw_pile) > 0:
            card = random.choice(player.deck.draw_pile)
            card.play(player, target_enemy, enemies, debug)
            card.play(player, target_enemy, enemies, debug)
            player.deck.exhaust_pile.append(card)
            if card in player.deck.draw_pile:
                player.deck.draw_pile.remove(card)
        # TODO notify exhaust listeners if needed

    def upgrade(self):
        super().upgrade()
        self.energy = 3
