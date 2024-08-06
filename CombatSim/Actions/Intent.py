from CombatSim.Actions.Playable import Playable


class Intent(Playable):
    def __init__(self, name, damage, attacks, block, probability):
        super().__init__(damage, attacks, block)
        self.probability = probability
        self.name = name

    def play(self, enemy, player, player_list, debug):
        if debug:
            print("Playing " + str(self) + "...")
        super().play(enemy, player, player_list, debug)

    def __str__(self):
        return "INTENT: " + self.name + " - " + super().__str__() + " Probability: " + str(self.probability)
