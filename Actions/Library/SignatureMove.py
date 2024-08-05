from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Listener import Listener


class SignatureMove(Card):
    def __init__(self, player: Player):
        super().__init__("SignatureMove", Card.Type.ATTACK, 2, 30, 1, 0, 0, 0, False, False, player, None)
        self.listener = Listener([Listener.Event.POWER_PLAYED, Listener.Event.SKILL_PLAYED, Listener.Event.ATTACK_PLAYED, Listener.Event.HAND_CHANGED], self.do_listen)
        player.add_listener(self.listener)
        self.do_listen(player, None, [], False)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Can only be played if this is the only attack in your hand. Deal 30(40) damage.

    def do_listen(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            if card != self and card.card_type == Card.Type.ATTACK:
                self.playable = False
                return

        self.playable = True

    def upgrade(self):
        super().upgrade()
        self.damage = 40
