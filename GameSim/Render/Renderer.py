import time
from enum import Enum

import pygame


class Renderer:
    class RenderType(Enum):
        NONE = 0
        PYGAME = 1

    def __init__(self, screen_size=(1280, 720), render_type=RenderType.PYGAME):
        self.render_type = render_type

        if self.do_render():
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("monospace", 20)
        else:
            self.screen = None
            self.clock = None
            self.font = None


        self.running = True
        self.debug = False
        self.screen_size = screen_size

        self.room_to_render = None

    def do_render(self):
        return self.render_type == self.RenderType.PYGAME

    def render_combat(self, combat, frames_per_action=60, end_delay=2):
        self.running = True
        counter = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            # pygame.draw.circle(self.screen, (255, 255, 255), (100, 100), 50, 25)
            self.running = combat.render_room(self.screen, self.screen_size, self.font)
            pygame.display.flip()
            self.clock.tick(60)
            counter += 1
        time.sleep(end_delay)

    def render_playable_combat(self, combat):
        self.running = True
        while self.running:
            self.running = combat.render_room(self.screen, self.screen_size, self.font)
            pygame.display.flip()
            self.clock.tick(60)

        time.sleep(4)
        pygame.quit()

    def render_act_map(self, map_gen, cur_floor, cur_idx):
        self.running = True
        map_font = pygame.font.SysFont("Arial", 20)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    map_gen.handle_event(event, self.screen_size, cur_floor, cur_idx)

            self.screen.fill((0, 0, 0))

            room_choice = map_gen.render(self.screen, self.screen_size, map_font, cur_floor, cur_idx)

            if room_choice is not None:
                self.running = False
                return room_choice

            pygame.display.flip()
            self.clock.tick(60)

    def render_room(self, room):
        self.running = True

        room_font = None
        if self.do_render():
            room_font = pygame.font.SysFont("Arial", 20)

        # room.start()
        while self.running:
            if self.do_render():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_render()
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        room.handle_event(event)

                self.screen.fill((0, 0, 0))
            self.running = room.render_room(self.screen, self.screen_size, room_font, self.render_type)

            if self.do_render():
                pygame.display.flip()
                self.clock.tick(60)

    def quit_render(self):
        pygame.quit()
        self.running = False
