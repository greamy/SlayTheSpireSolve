from GameSim.Input.Controller import PlayerController


class RLPlayerController(PlayerController):

    def __init__(self, delay=0, train=True):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60

        self.train = train

    def get_target(self, player, enemies, playable, debug):
        pass

    def get_scry(self, player, enemies, cards, debug):
        pass

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        pass


