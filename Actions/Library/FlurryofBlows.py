from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class FlurryofBlows(Card):
    def __init__(self, player: Player):
        super().__init__("FlurryofBlows", Card.Type.ATTACK, 0, 4, 1, 0, 0, 0, False, False, player, None)
        self.card_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_card)
        self.last_stance = None
        player.add_listener(self.card_listener)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.

    def do_card(self, player, enemy, enemies, debug):
        if self.last_stance != player.stance and len(player.deck.hand) < 10 and self in player.deck.discard_pile:
            player.deck.discard_pile.remove(self)
            player.deck.hand.append(self)

        self.last_stance = player.stance

    def upgrade(self):
        super().upgrade()
        self.damage = 6
