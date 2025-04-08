
class Relic:


    def __init__(self, name: str, rarity: str, player):
        self.name = name
        self.rarity = rarity
        self.player = player


    def on_pickup(self):
        """
        Runs any or 'on-pickup' effects and applies listeners needed for combat effects

        :return: None
        """
        pass

    def on_drop(self):
        """
        Define what happens when we lose the relic

        :return: None
        """
        pass

