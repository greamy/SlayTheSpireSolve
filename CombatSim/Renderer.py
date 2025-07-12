import random
import time
import pygame


class Renderer:

    def __init__(self, combat, screen_size=(1280, 720)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("monospace", 20)
        self.combat = combat
        self.debug = False

        self.end_turn_x = 525
        self.end_turn_y = 300
        self.end_turn_width = 160
        self.end_turn_height = 80

    def render_combat(self):
        counter = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            # pygame.draw.circle(self.screen, (255, 255, 255), (100, 100), 50, 25)
            if counter % 60 == 0:
                self.running = self.combat.do_next_turn()
            self.combat.renderall(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            counter += 1
        time.sleep(2)
        pygame.quit()

    def render_playable_combat(self):
        counter = 0
        fail_msg = None
        fail_msg_counter = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.combat.current_turn == self.combat.PLAYER_TURN:
                        # get position of mouse click
                        pos = pygame.mouse.get_pos()

                        if self.end_turn_x < pos[0] < self.end_turn_x + self.end_turn_width and \
                            self.end_turn_y < pos[1] < self.end_turn_y + self.end_turn_height:
                            self.combat.player.turn_over = True
                            continue

                        # check if any card was clicked
                        for card in self.combat.player.deck.hand:
                            if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                                # play the card
                                enemy = random.choice(self.combat.enemies)
                                success = self.combat.player.play_card(card, enemy, self.combat.enemies, self.debug)
                                if not success:
                                    print("Card play failed")
                                    fail_msg = self.font.render("Card play failed", True, (255, 0, 0))

            if self.combat.player.check_turn_done():
                self.combat.player.end_turn(self.combat.enemies, self.debug)

                self.combat.current_turn = self.combat.ENEMY_TURN

            if self.combat.get_total_enemy_health() <= 0:
                self.combat.player_won = True
                self.running = False

            pos = pygame.mouse.get_pos()
            # check if any card was clicked
            help_box_x = 50
            help_box_y = 260
            help_box_width = 325
            help_box_height = 175
            card_hovered = None
            for card in self.combat.player.deck.hand:
                if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                    # show info about the card
                    card_hovered = card

            self.screen.fill((0, 0, 0)) # SCREEN CLEARING IS HAPPENING HERE!!! BE CAREFUL

            if card_hovered is not None:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (help_box_x, help_box_y, help_box_width, help_box_height),
                                 0, 2)
                name = self.font.render(card_hovered.name, True, (0, 0, 0))
                self.screen.blit(name, (help_box_x+5, help_box_y+10))
                cost = self.font.render("Energy: " + str(card_hovered.energy), True, (0, 255, 0))
                self.screen.blit(cost, (help_box_x + help_box_width - 125, help_box_y + 10))

                # separate description into 20 characters per line
                description_lines = []
                description_text = card_hovered.description
                while len(description_text) > 25:
                    line = description_text[:25]
                    description_lines.append(line)
                    description_text = description_text[25:]
                description_lines.append(description_text)

                for i, line in enumerate(description_lines):
                    text = self.font.render(line, True, (255, 100, 50))
                    self.screen.blit(text, (help_box_x + 5, help_box_y + 30 + (i * 20)))

            if fail_msg is not None:
                self.screen.blit(fail_msg, (300, 300))
                fail_msg_counter += 1
                if fail_msg_counter == 60:
                    fail_msg = None
                    fail_msg_counter = 0

            # pygame.draw.circle(self.screen, (255, 255, 255), (100, 100), 50, 25)
            if self.combat.current_turn == self.combat.ENEMY_TURN:
                if counter == 60:
                    self.running = self.combat.do_next_turn()
                    counter = 0
                else:
                    counter += 1
            else:
                counter = 0

            pygame.draw.rect(self.screen, (100, 175, 100),
                             (self.end_turn_x, self.end_turn_y, self.end_turn_width, self.end_turn_height), 0, 5)
            font = pygame.font.SysFont("monospace", 30)
            end_turn_text = font.render("End Turn", True, (0, 0, 0))
            self.screen.blit(end_turn_text, (self.end_turn_x + 5, self.end_turn_y + 5))

            self.combat.renderall(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        time.sleep(4)
        pygame.quit()

    def render_map(self, map_gen):
        map_font = pygame.font.SysFont("Arial", 20)
        regen_btn_x = 750
        regen_btn_y = 25
        regen_btn_width = 200
        regen_btn_height = 50
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if regen_btn_x < pos[0] < regen_btn_x + regen_btn_width and \
                           regen_btn_y < pos[1] < regen_btn_y + regen_btn_height:
                            map_gen.generate_map()

            self.screen.fill((0, 0, 0))
            map_gen.render(self.screen, map_font)

            pygame.draw.rect(self.screen, (100, 255, 125), (regen_btn_x, regen_btn_y, 200, 50), 0, 5)
            regen_btn_txt = self.font.render("Re-Generate Map", True, (0, 0, 0))
            self.screen.blit(regen_btn_txt, (regen_btn_x + 10, regen_btn_y + 10))

            pygame.display.flip()
            self.clock.tick(60)
