import random
import time
import pygame


class Renderer:

    def __init__(self, screen, combat):
        self.screen = screen
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
            help_box_x = 100
            help_box_y = 300
            help_box_width = 250
            help_box_height = 100
            card_hovered = None
            for card in self.combat.player.deck.hand:
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