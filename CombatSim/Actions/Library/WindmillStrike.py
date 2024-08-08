from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class WindmillStrike(Card):
    def __init__(self, player: Player):
        super().__init__("WindmillStrike", Card.Type.ATTACK, 2, 7, 1, 0, 0, 0, False, True, player, None)
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_retain)
        player.add_listener(self.listener)
        self.damage_increase = 4
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # {{Retain}}. Deal 7(10) damage. Whenever this card is {{Retained}}, increase its damage by 4(5).
        super().play(player, target_enemy, enemies, debug)

    def do_retain(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        if self in player.deck.hand:
            self.damage += self.damage_increase

    def upgrade(self):
        super().upgrade()
        self.damage = 10
        self.damage_increase = 5
