import random
import time
import pygame

from GameSim.Map.MapGenerator import MapGenerator


class Renderer:

    def __init__(self, screen_size=(1280, 720)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("monospace", 20)
        self.debug = False
        self.screen_size = screen_size

        self.room_to_render = None

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

    # def render_map(self, map_gen):
    #     self.running = True
    #     room_choice = None
    #     map_font = pygame.font.SysFont("Arial", 20)
    #     regen_btn_x = 750
    #     regen_btn_y = 25
    #     regen_btn_width = 200
    #     regen_btn_height = 50
    #     while self.running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.running = False
    #
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 if event.button == 1:
    #                     pos = pygame.mouse.get_pos()
    #                     if regen_btn_x < pos[0] < regen_btn_x + regen_btn_width and \
    #                        regen_btn_y < pos[1] < regen_btn_y + regen_btn_height:
    #                         map_gen.generate_map()
    #
    #                     for floor in map_gen.map:
    #                         for room in floor:
    #                             if room is not None:
    #                                 room_x, room_y = map_gen.calculate_position_from_idx(room.floor, room.x, self.screen_size)
    #                                 if room_x < pos[0] < room_x + map_gen.tile_size and room_y < pos[1] < room_y + map_gen.tile_size:
    #                                     room_choice = room
    #
    #         self.screen.fill((0, 0, 0))
    #
    #         if room_choice is not None:
    #             return room_choice
    #
    #         map_gen.render(self.screen, self.screen_size, map_font, 0, 0)
    #
    #         pygame.draw.rect(self.screen, (100, 255, 125), (regen_btn_x, regen_btn_y, 200, 50), 0, 5)
    #         regen_btn_txt = self.font.render("Re-Generate Map", True, (0, 0, 0))
    #         self.screen.blit(regen_btn_txt, (regen_btn_x + 10, regen_btn_y + 10))
    #
    #         pygame.display.flip()
    #         self.clock.tick(60)

    def render_room(self, room):
        self.running = True
        room_font = pygame.font.SysFont("Arial", 20)
        room.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_render()
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    room.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.running = room.render_room(self.screen, self.screen_size, room_font)

            pygame.display.flip()
            self.clock.tick(60)

    def quit_render(self):
        pygame.quit()
        self.running = False
