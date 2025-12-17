from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class FlurryofBlows(Card):
    def __init__(self, player: Player):
        super().__init__("FlurryofBlows", Card.Type.ATTACK, 0, 4, 1, 0, 0, 0, False, False, player, None, id=33)
        self.description = "Deal 4 damage. On Stance change, returns from the Discard Pile into your hand."
        self.card_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_card)
        self.last_stance = player.stance
        player.add_listener(self.card_listener)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.
        self.last_stance = player.stance

        return True

    def do_card(self, player, enemy, enemies, debug):
        if self.last_stance != player.stance and len(player.deck.hand) < 10 and self in player.deck.discard_pile:
            player.deck.discard_pile.remove(self)
            player.deck.hand.append(self)
            player.notify_listeners(Listener.Event.HAND_CHANGED, player, enemies, debug)

        self.last_stance = player.stance

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 6 damage. On Stance change, returns from the Discard Pile into your hand."
        self.damage = 6

    def remove_listeners(self, player: Player):
        if self.card_listener in player.listeners:
            player.remove_listener(self.card_listener)
        super().remove_listeners(player)
