from GameSim.BotTraining.Regimen import Regimen
from GameSim.Input import Controller
from GameSim.Input.RLPlayerController import RLPlayerController
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, addCards, get_default_deck

class Trainer:

    def __init__(self, renderer: Renderer, agent_save_path="artifacts/images/model_results/first_fight/"):
        self.renderer = renderer
        self.controller = RLPlayerController(agent_save_path, delay=0, train=True)
        # self.player = self.get_player(self.controller)

        self.act = 1
        self.ascension = 20

        self.curriculum: list[Regimen] = []

    def add_regimen(self, regimen: Regimen):
        self.curriculum.append(regimen)

    def run(self):
        for reg in self.curriculum:
            player = reg.get_player(self.controller)
            rooms = reg.get_rooms(player)
            for idx, room in enumerate(rooms):
                self.renderer.render_room(room)

                # TODO: Collect reward logs and generate graphs if needed
                # TODO: implement early-stopping somehow to stop running episodes if reward has stagnated


