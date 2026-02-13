from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Burn(Card):
    def __init__(self, player: Player):
        super().__init__("Burn", Card.Type.STATUS, 0, 0, 0, 0, 0, 0, False, False, player, None, id=7)
        self.description = "Unplayable. At the end of your turn take 2 damage."
        self.playable = False
        self.end_of_turn_damage = 2
        player.add_listener(Listener(Listener.Event.END_TURN, self.eot_take_damage))

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Unplayable. At the end of your turn take 2 (4) damage.
        super().play(player, player_list, target_enemy, enemies, debug)

        return True

    def upgrade(self):
        self.description = "Unplayable. At the end of your turn take 4 damage."
        self.end_of_turn_damage = 4

    def eot_take_damage(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        if self in player.deck.hand:
            lost_health = player.take_damage(self.end_of_turn_damage)
            if lost_health:
                player.notify_listeners(Listener.Event.TAKEN_DAMAGE, enemy, enemies, debug)
