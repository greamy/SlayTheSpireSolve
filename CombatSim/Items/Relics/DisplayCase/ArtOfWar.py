from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class ArtOfWar(Relic):
    # If you do not play any Attacks during your turn, gain an extra Energy next turn.
    def __init__(self, player):
        super().__init__("Art of War", "Common", player)
        self.player = player
        self.attack_played = False
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.attack_was_played)
        self.turn_over = Listener(Listener.Event.START_TURN, self.start_of_turn)

    def attack_was_played(self, player, enemy, enemies, debug):
        self.attack_played = True

    def on_pickup(self):
        self.player.add_listener(self.attack_listener)
        self.player.add_listener(self.turn_over)

    def on_drop(self):
        self.player.remove_listener(self.attack_listener)
        self.player.remove_listener(self.turn_over)

    def start_of_turn(self, player, enemy, enemies, debug):
        if not self.attack_played:
            player.energy += 1
        self.attack_played = False

