from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener


class SignatureMove(Card):
    def __init__(self, player: Player):
        super().__init__("SignatureMove", Card.Type.ATTACK, 2, 30, 1, 0, 0, 0, False, False, player, None, id=66)
        self.listener = Listener([Listener.Event.POWER_PLAYED, Listener.Event.SKILL_PLAYED, Listener.Event.ATTACK_PLAYED, Listener.Event.HAND_CHANGED], self.do_listen)
        player.add_listener(self.listener)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Can only be played if this is the only attack in your hand. Deal 30(40) damage.
        super().play(player, player_list, target_enemy, enemies, debug)

    def do_listen(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            if card != self and card.card_type == Card.Type.ATTACK:
                self.playable = False
                return

        self.playable = True

    def upgrade(self):
        super().upgrade()
        self.damage = 40
