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
        # self.cur_floor = 0
        # self.cur_idx = None

        # self.map_gen = MapGenerator(self.player, self.act, self.ascension)
        # self.map_gen.generate_map()
        # self.map = self.map_gen.map
        self.curriculum: list[Regimen] = []

    def add_regimen(self, regimen: Regimen):
        self.curriculum.append(regimen)

    def run(self):
        for reg in self.curriculum:
            player = reg.get_player(self.controller)
            for episode in range(reg.num_episodes):
                room = reg.get_room(player)
                room.start()
                self.renderer.render_room(room)
                if not player.is_alive():
                    player = reg.get_player(self.controller)

                # TODO: Collect reward logs and generate graphs if needed
                # TODO: implement early-stopping somehow to stop running episodes if reward has stagnated


