from CombatSim.Entities.Player import Player
from GameSim.Map.Event import Event, EventOption


class Lab(Event):
    title = "Lab"
    description = (
        "You find yourself in a room filled with racks of test tubes, beakers, flasks, forceps, pinch clamps,"
        "stirring rods, tongs, goggles, funnels, pipets, cylinders, condensers, and even a rare spiral tube of glass."
        "Why do you know the name of all these tools? It doesn't matter, you take a look around."
    )

    def __init__(self, player, act, ascension):
        super().__init__(player, act, ascension)

    def build_options(self):
        return [
            EventOption("Search", "Obtain 3 (2) random Potions.", self.search),
            EventOption("Leave", ""),
        ]

    def search(self, player):
        # TODO: Implement potions:
        pass

    def leave(self, player):
        pass
