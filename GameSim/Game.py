from GameSim.Input import Controller
from GameSim.Map.MapGenerator import MapGenerator
from GameSim.Map.MonsterRoom import MonsterRoom
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, addCards, get_default_deck

class Game:

    def __init__(self, controller: Controller, renderer: Renderer):
        self.renderer = renderer
        self.player = self.get_player(controller)

        self.act = 1
        self.ascension = 0
        self.cur_floor = 0
        self.cur_idx = None

        self.map_gen = MapGenerator(self.player, self.act, self.ascension)
        self.map_gen.generate_map()
        self.map = self.map_gen.map

    def get_player(self, controller: Controller):
        # TODO: render a character select screen then create a self.player with correct health and starting relic.
        self.player = createPlayer(controller=controller)
        addCards(self.player, get_default_deck())
        return self.player

    def run(self):
        # TODO: do neow room
        for i in range(15):
            room = self.renderer.render_act_map(self.map_gen, self.cur_floor, self.cur_idx)
            self.renderer.render_room(room)
            self.cur_floor += 1
            self.cur_idx = room.x
