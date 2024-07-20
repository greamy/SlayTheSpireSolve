from Actions.Playable import Playable


class Intent(Playable):
    def __init__(self, damage, attacks, block, status, probability):
        super().__init__(damage, attacks, block, status)
        self.probability = probability

    def play(self, enemy, player, debug):
        if debug:
            print("Playing " + str(self) + "...")
        super().play(enemy, player, debug)

    def __str__(self):
        return "INTENT: " + super().__str__() + " Probability: " + str(self.probability)
