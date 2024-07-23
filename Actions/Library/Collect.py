from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Library.Miracle import Miracle


class Collect(Card):
    def __init__(self):
        super().__init__("Collect", Card.Type.SKILL, 0, 0, 0, 0, 0, 0, True, False, "", None)
        self.listener = Listener(Listener.Event.START_TURN, self.do_skill, 0)
        self.x_modifier = 0
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        self.listener.num_turns = player.energy + self.x_modifier
        player.energy = 0
        player.add_listener(self.listener)
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.

    def do_skill(self, player, enemy, enemies, debug):
        player.deck.hand.append(Miracle())

    def upgrade(self):
        super().upgrade()
        self.x_modifier = 1
