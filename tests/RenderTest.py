import importlib
import time
import unittest
import pygame

from Combat import Combat
from CombatSim.Entities.Player import Player


class RenderTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        self.energy = 3
        self.health = 72
        self.gold = 690
        self.potions = []
        self.relics = []
        self.debug = False

        self.cards = ["Strike" for _ in range(4)]
        self.cards.extend(["Defend" for _ in range(4)])
        self.cards.extend(["Vigilance", "Eruption"])
        self.cards.extend(["Devotion" for _ in range(5)])
        self.cards.extend(["SandsofTime" for _ in range(2)])

        self.player = self.createPlayer()
        self.addCards(self.cards)

        self.enemy = self.createEnemy("SlimeBoss", 20, 1)

    def addCards(self, name_list: list[str]):
        cards = []
        for name in name_list:
            module = importlib.import_module("CombatSim.Actions.Library." + name)
            class_ = getattr(module, name)
            card = class_(self.player)
            cards.append(card)
        self.player.deck = Player.Deck(cards)

    def createPlayer(self):
        return Player(self.health, self.energy, self.gold, self.potions, self.relics, self.cards,
                      "../CombatSim/Actions/Library")

    def createEnemy(self, name: str, ascension: int, act: int):
        module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
        class_ = getattr(module, name)
        return class_(ascension, act)

    def test_render(self):
        counter = 0
        testing_enemy = self.createEnemy("SlimeBoss", 20, 1)
        testing_player = self.createPlayer()
        combat = Combat(testing_player, [testing_enemy], True)
        combat.start()
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            # pygame.draw.circle(self.screen, (255, 255, 255), (100, 100), 50, 25)
            if counter % 60 == 0:
                self.running = combat.do_next_turn()
            combat.renderall(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            counter += 1
        time.sleep(2)
        pygame.quit()