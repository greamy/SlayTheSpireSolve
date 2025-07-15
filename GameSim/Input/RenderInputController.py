import random
import pygame

from GameSim.Input.Controller import PlayerController


class RenderInputPlayerController(PlayerController):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.scry_done = False
        self.to_discard = set()
        self.card_selected = None
        self.enemy_selected = None

    def reset(self):
        self.card_selected = None
        self.enemy_selected = None

    def handle_event(self, pos, player, enemies):
        for i, enemy in enumerate(enemies):
            if enemy.x < pos[0] < enemy.x + enemy.width and enemy.y < pos[1] < enemy.y + enemy.height:
                self.enemy_selected = i

        for i, card in enumerate(player.deck.hand):
            if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                self.card_selected = i

    def get_target(self, player, enemies, playable, debug):
        i = None
        enemy = None
        if self.enemy_selected is not None:
            enemy = enemies[self.enemy_selected]
            i = self.enemy_selected
        return i, enemy

    def get_scry(self, player, enemies, scry_cards, debug):
        card_font = pygame.font.SysFont("Arial", 20)
        scry_window_x = 100
        scry_window_y = 200
        scry_window_width = 400
        scry_window_height = 250

        done_button_x = scry_window_x + scry_window_width - 100
        done_button_y = scry_window_y + scry_window_height - 75
        done_button_width = 100
        done_button_height = 50

        # Main Window
        pygame.draw.rect(self.screen, (255, 255, 255), (scry_window_x, scry_window_y,
                                                        scry_window_width, scry_window_height), 2, 3)
        pygame.draw.rect(self.screen, (0, 0, 0), (scry_window_x-5, scry_window_y-5,
                                                  scry_window_width-5, scry_window_height-5), 0, 3)

        # scry complete button
        pygame.draw.rect(self.screen, (25, 255, 25), (done_button_x, done_button_y, done_button_width,
                                                      done_button_height), 0, 2)

        for i, card in enumerate(scry_cards):
            card.y = scry_window_y + 10
            card.start_x = scry_window_x + 10
            card.render(self.screen, card_font, i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if done_button_x < pos[0] < done_button_x + done_button_width and done_button_y < pos[1] < done_button_y + done_button_height:
                        return self.to_discard

                    for i, card in enumerate(scry_cards):
                        if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                            if card in self.to_discard:
                                self.to_discard.remove(i)
                            else:
                                self.to_discard.add(i)
        return None

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        card = None
        i = None
        if self.card_selected is not None:
            card = player.deck.hand[self.card_selected]
            i = self.card_selected
        return i, card
