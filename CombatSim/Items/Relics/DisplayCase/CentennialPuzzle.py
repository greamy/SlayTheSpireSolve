from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class CentennialPuzzle(Relic):
    # The first time you lose HP each combat, draw 3 cards.
    DRAW_AMT = 3
    def __init__(self, player):
        super().__init__("Centennial Puzzle", "Common", player)
        self.start_combat_listener = Listener(Listener.Event.START_COMBAT, self.start_combat)
        self.lose_hp_listener = Listener(Listener.Event.TAKEN_DAMAGE, self.lose_hp)
        self.lost_hp_yet = False

    def start_combat(self, player, enemy, enemies, debug):
        self.lost_hp_yet = False

    def lose_hp(self, player, enemy, enemies, debug):
        if not self.lost_hp_yet:
            self.player.draw_cards(self.DRAW_AMT, enemies, debug)

        self.lost_hp_yet = True

    def on_pickup(self):
        self.player.add_listener(self.start_combat_listener)
        self.player.add_listener(self.lose_hp_listener)

    def on_drop(self):
        self.player.remove_listener(self.start_combat_listener)
        self.player.remove_listener(self.lose_hp_listener)