import time
import unittest

from Combat import Combat
from CombatSim.Map.MapGenerator import MapGenerator
from CombatSim.Map.RestRoom import RestRoom
from CombatSim.Renderer import Renderer
from CombatSim.util import addCards, createPlayer, createEnemy, get_default_deck


class RenderTest(unittest.TestCase):

    def setUp(self):

        self.debug = False

        cards = get_default_deck()
        self.player = createPlayer()
        addCards(self.player, cards)

        self.enemy = createEnemy("JawWorm", 20, 1)
        # self.enemy_2 = createEnemy("GreenLouse", 20, 1)
        self.combat = Combat(self.player, [self.enemy], True)
        self.renderer = Renderer(self.combat)

    def test_render(self):
        self.combat.start()
        renderer = Renderer(self.combat)
        renderer.render_combat()
        renderer.quit_render()

    def test_fast_render(self):
        combats = [Combat(createPlayer(), [createEnemy('JawWorm', i, 3)], False) for i in range(20)]
        renderer = Renderer(combats[0])
        num_won = 0
        default_deck = get_default_deck()
        start = time.time()
        for combat in combats:
            addCards(combat.player, default_deck)
            combat.start()

            renderer.combat = combat
            renderer.render_combat(frames_per_action=1, end_delay=0)
            num_won += 1 if renderer.combat.player_won else 0
        end = time.time()

        print(f"Number of combats won: {num_won} out of {len(combats)}")
        print(f"Time elapsed: {end - start} seconds")
        renderer.quit_render()

    def test_playable_render(self):
        self.combat.start()

        renderer = Renderer(self.combat, (1280, 720))
        renderer.render_playable_combat()

    def test_render_map(self):
        map_gen = MapGenerator()
        map_gen.generate_map()
        # paths = map_gen.generate_paths()
        # _, map_gen.map = map_gen.populate_map_with_paths(paths)

        renderer = Renderer(self.combat)
        renderer.render_map(map_gen)

    def test_render_rest(self):
        rest = RestRoom(0, 0, [], [])

        renderer = Renderer(self.combat)
        renderer.render_room(rest)

