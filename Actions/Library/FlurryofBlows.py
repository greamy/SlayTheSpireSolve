from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class FlurryofBlows(Card):
    def __init__(self):
        super().__init__("FlurryofBlows", Card.Type.ATTACK, 0, 4, 1, 0, 0, 0, False, False, "", None)
        self.card_listener = Listener(Listener.Event.CARD_PLAYED, self.do_card)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.

    def do_card(self, player, enemy, enemies, debug, card_played):
        if self in player.deck.discard_pile:
            if len(player.deck.hand) < 10:
                if player.card.stance in player.play_card(card_played) != player.Stance:
                    player.deck.discard_pile.remove(self)
                    player.deck.hand.append(self)

    def upgrade(self):
        super().upgrade()
        self.damage = 6
