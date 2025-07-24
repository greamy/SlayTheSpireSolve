import time
import unittest

from GameSim.Input.RenderInputController import RenderInputPlayerController
from GameSim.Map.CombatRoom import CombatRoom
from GameSim.Map.MapGenerator import MapGenerator
from GameSim.Map.RestRoom import RestRoom
from GameSim.Render.Renderer import Renderer
from CombatSim.util import addCards, createPlayer, createEnemy, get_default_deck


class RenderTest(unittest.TestCase):

    def setUp(self):
        self.debug = False

        self.act = 1
        self.ascension = 0

        self.screen_size = (1280, 720)
        self.renderer = Renderer(self.screen_size)

        cards = get_default_deck()
        self.player = createPlayer(controller=RenderInputPlayerController(self.renderer.screen))
        addCards(self.player, cards)

        self.enemy = createEnemy("JawWorm", 20, 1)
        # self.enemy_2 = createEnemy("GreenLouse", 20, 1)
        self.combat = CombatRoom(self.player, 'M', 0, 0, [], [], 0, 0)


    def test_render(self):
        self.combat.start()
        self.renderer.render_combat(self.combat)
        self.renderer.quit_render()

    def test_fast_render(self):
        combats = [CombatRoom(createPlayer(), 'M', 0, 0, [], [], 0, 0) for i in range(20)]
        num_won = 0
        default_deck = get_default_deck()
        start = time.time()
        for combat in combats:
            addCards(combat.player, default_deck)
            combat.start()

            self.renderer.render_combat(combat, frames_per_action=1, end_delay=0)
            num_won += 1 if combat.player_won else 0
        end = time.time()

        print(f"Number of combats won: {num_won} out of {len(combats)}")
        print(f"Time elapsed: {end - start} seconds")
        self.renderer.quit_render()

    def test_playable_render(self):
        self.combat.start()

        self.renderer.render_room(self.combat)

    def test_render_map(self):
        map_gen = MapGenerator(self.player, self.act, self.ascension)
        map_gen.generate_map()
        # paths = map_gen.generate_paths()
        # _, map_gen.map = map_gen.populate_map_with_paths(paths)

        self.renderer.render_act_map(map_gen, 0, None)

    def test_render_rest(self):
        rest = RestRoom(0, 0, [], [])

        self.renderer.render_room(rest)

