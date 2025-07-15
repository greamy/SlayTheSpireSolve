from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card



class DevaForm(Card):
    def __init__(self, player: Player):
        super().__init__("DevaForm", Card.Type.POWER, 3, 0, 0, 0, 0, 0, False, False, player, None, id=22)
        self.description = "Ethereal. At the start of your turn, gain Energy and increase this gain by 1.)"
        self.energy_listener = Listener(Listener.Event.START_TURN, self.do_power)
        self.ethereal_listener = Listener(Listener.Event.END_TURN, self.do_ethereal)
        player.add_listener(self.ethereal_listener)
        self.ethereal = True
        self.extra_energy = 1

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)
        player.add_listener(self.energy_listener)

        return True

    def do_power(self, player, enemy, enemies, debug):
        player.energy += self.extra_energy
        self.extra_energy += 1

    def do_ethereal(self, player, enemy, enemies, debug):
        if self.ethereal and self in player.deck.hand:
            player.deck.hand.remove(self)
            player.deck.exhaust_pile.append(self)

    def upgrade(self):
        super().upgrade()
        self.description = "At the start of your turn, gain Energy and increase this gain by 1.)"
        self.ethereal = False
