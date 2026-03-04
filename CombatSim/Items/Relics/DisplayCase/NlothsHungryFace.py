from CombatSim.Items.Relics.Relic import Relic


class NlothsHungryFace(Relic):
    # The next non-boss chest you open is empty.
    # Sets player.next_chest_empty = True; ChestRoom is responsible for checking
    # and clearing this flag when a chest is opened.
    def __init__(self, player):
        super().__init__("NlothsHungryFace", "Event", player)

    def on_pickup(self):
        self.player.next_chest_empty = True

    def on_drop(self):
        self.player.next_chest_empty = False