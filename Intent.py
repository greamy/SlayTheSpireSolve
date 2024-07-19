from Playable import Playable


class Intent(Playable):
    def __init__(self, damage, attacks, block, status, probability):
        super().__init__(damage, attacks, block, status)
        self.probability = probability
