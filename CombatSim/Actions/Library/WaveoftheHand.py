from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Entities.Weak import Weak


class WaveoftheHand(Card):
    def __init__(self, player: Player):
        super().__init__("WaveoftheHand", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener(Listener.Event.BLOCK_GAINED, self.block_gained)
        self.end_listener = Listener(Listener.Event.END_TURN, self.end_card)
        self.weak = 1
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever you gain {{Block}} this turn, apply 1(2) {{Weak}} to ALL enemies
        player.add_listener(self.listener)
        player.add_listener(self.end_listener)

    def block_gained(self, player, enemy, enemies, debug):
        weak = Weak(self.weak, enemy)
        enemy.add_listener(Listener(Listener.Event.START_TURN, weak.decrement))

    def end_card(self, player, enemy, enemies, debug):
        player.listeners.remove(self.listener)
        player.listeners.remove(self.end_listener)

    def upgrade(self):
        super().upgrade()
        self.weak = 2