from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class Omniscience(Card):
    def __init__(self, player: Player):
        super().__init__("Omniscience", Card.Type.SKILL, 4, 0, 0, 0, 0, 0, True, False, player, None, id=52)
        self.description = "Choose a card in your draw pile. Play the chosen card twice and Exhaust it. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. {{Exhaust}}.
        # TODO: make not random
        if len(player.deck.draw_pile) > 0:
            card = random.choice(player.deck.draw_pile)
            if not card.playable:
                player.deck.exhaust_pile.append(player.deck.draw_pile)
                player.deck.draw_pile.remove(card)
                return
            card.play(player, player_list, target_enemy, enemies, debug)
            card.play(player, player_list, target_enemy, enemies, debug)
            player.deck.exhaust_pile.append(card)
            if card in player.deck.draw_pile:
                player.deck.draw_pile.remove(card)
        # TODO notify exhaust listeners if needed

    def upgrade(self):
        super().upgrade()
        self.description = "Choose a card in your draw pile. Play the chosen card twice and Exhaust it. Exhaust."
        self.energy = 3
