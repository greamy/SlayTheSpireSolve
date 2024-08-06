from Actions.Library.Miracle import Miracle
from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class DeusExMachina(Card):
    def __init__(self, player: Player):
        super().__init__("DeusExMachina", Card.Type.SKILL, None, 0, 0, 0, 0, 0, True, False, player, None)
        self.listener = Listener(Listener.Event.HAND_CHANGED, self.do_draw)
        player.add_listener(self.listener)
        self.playable = False
        self.num_cards = 2
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # {{Unplayable}}. When you draw this card, add 2(3) {{C|Miracle|Miracles}} into your hand. {{Exhaust}}.
        raise RuntimeError("DeusExMachina is unplayable!")


    def do_draw(self, player, enemy, enemies, debug):
        num_cards = self.num_cards
        if self in player.deck.hand:
            if len(player.deck.hand) + 2 > Player.Deck.MAX_HAND_SIZE:
                num_cards = Player.Deck.MAX_HAND_SIZE - len(player.deck.hand)
            player.deck.hand.extend([Miracle(player) for _ in range(num_cards)])
