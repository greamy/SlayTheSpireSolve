from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class ArtOfWar(Relic):
    # If you do not play any Attacks during your turn, gain an extra Energy next turn.
    def __init__(self, player):
        super().__init__("Art of War", "Common", player)
        self.player = player
        self.attack_played = False
        self.listener = Listener(Listener.Event.ATTACK_PLAYED, self.attack_was_played)
        self.turn_over = Listener(Listener.Event.START_TURN, self.start_of_turn)

    def attack_was_played(self):
        self.attack_played = True

    def start_of_turn(self, player, enemy, enemies, debug):
        if not self.attack_played:
            self.player.energy += 1
        self.attack_played = False

