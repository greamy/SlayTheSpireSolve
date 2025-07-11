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
        self.font = pygame.font.SysFont("monospace", 20)

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
        testing_enemy = self.createEnemy("Hexaghost", 20, 1)
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

    def test_playable_render(self):
        counter = 0
        enemy = self.createEnemy("AcidSlimeSmall", 20, 1)
        player = self.createPlayer()
        combat = Combat(player, [enemy], True)
        combat.start()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and combat.current_turn == combat.PLAYER_TURN:
                        # get position of mouse click
                        pos = pygame.mouse.get_pos()
                        # check if any card was clicked
                        for card in player.deck.hand:
                            if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                                # play the card
                                success = player.play_card(card, enemy, [enemy], self.debug)
                                if not success:
                                    print("Card play failed")
                                    fail_msg = self.font.render("Card play failed", True, (255, 0, 0))
                                    self.screen.blit(fail_msg, (300, 300))

            if player.check_turn_done():
                player.end_turn([enemy], self.debug)

                combat.current_turn = combat.ENEMY_TURN

            if combat.get_total_enemy_health() <= 0:
                combat.player_won = True
                self.running = False

            pos = pygame.mouse.get_pos()
            # check if any card was clicked
            help_box_x = 100
            help_box_y = 300
            help_box_width = 250
            help_box_height = 100
            card_hovered = None
            for card in player.deck.hand:
                if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                    # show info about the card
                    card_hovered = card

            self.screen.fill((0, 0, 0)) # SCREEN CLEARING IS HAPPENING HERE!!! BE CAREFUL

            if card_hovered is not None:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (help_box_x, help_box_y, help_box_width, help_box_height),
                                 100, 2)
                dmg = self.font.render("D:" + str(card_hovered.damage) + " * " + str(card_hovered.attacks), True,
                                       (255, 0, 0))
                self.screen.blit(dmg, (help_box_x + 5, help_box_y + 5))
                block = self.font.render("B:" + str(card_hovered.block), True, (0, 255, 0))
                self.screen.blit(block, (help_box_x + 5, help_box_y + 25))
                stance_str = str(card_hovered.stance).split('.')[1] if card_hovered.stance is not None else "None"
                stance = self.font.render("Stance: " + stance_str, True, (0, 0, 255))
                self.screen.blit(stance, (help_box_x + 5, help_box_y + 45))

            # pygame.draw.circle(self.screen, (255, 255, 255), (100, 100), 50, 25)
            if combat.current_turn == combat.ENEMY_TURN:
                if counter % 60 == 0:
                    self.running = combat.do_next_turn()
                    counter = 1
                else:
                    counter += 1
            else:
                counter = 0
            combat.renderall(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        time.sleep(4)
        pygame.quit()
