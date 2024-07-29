from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card



class DevaForm(Card):
    def __init__(self):
        super().__init__("DevaForm", Card.Type.POWER, 3, 0, 0, 0, 0, 0, False, False, "", None)
        self.energy_listener = Listener(Listener.Event.START_TURN, self.do_power)
        self.ethereal_listener = Listener(Listener.Event.END_TURN, self.do_ethereal)
        self.ethereal = True

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)

    def do_power(self, player, enemy, enemies, debug):
        extra_energy = 1
        player.energy += extra_energy
        extra_energy += 1

    def do_ethereal(self, player, enemy, enemies, debug):
        if self in player.deck.hand:
            player.deck.hand.remove(self)
            player.deck.exhaust_pile.append(self)

