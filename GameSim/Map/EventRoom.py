import random

import pygame

from CombatSim.Actions.Listener import Listener
from GameSim.Map.Event import Event, PlaceholderEvent
from GameSim.Map.Room import Room
from GameSim.Render.Renderer import Renderer


class EventRoom(Room):
    # Registry: call EventRoom.register_event(MyEvent) to add events to the pool.
    _event_pool: list[type[Event]] = []

    @classmethod
    def register_event(cls, event_cls: type[Event]):
        if event_cls not in cls._event_pool:
            cls._event_pool.append(event_cls)

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "?", floor, x, prev_rooms, next_rooms, act, ascension)
        self.color = (0, 255, 255)
        self.enemies = []

        self.event: Event | None = None

        # Layout constants (pygame mode)
        self._btn_w = 420
        self._btn_h = 50
        self._btn_x = 50
        self._desc_y = 100
        self._btn_y_start = 220
        self._btn_gap = 65

    # ------------------------------------------------------------------ #
    # Room interface                                                        #
    # ------------------------------------------------------------------ #

    def start(self):
        pool = self._event_pool if self._event_pool else [PlaceholderEvent]
        self.event = random.choice(pool)(self.player, self.act, self.ascension)
        self.player.notify_listeners(Listener.Event.ENTER_EVENT, self.player, None, False)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font, render_type):
        if self.event is None:
            self.start()

        if render_type == Renderer.RenderType.NONE:
            if not self.event.done:
                idx = self.player.controller.select_event_option(self.player, self.event)
                self.event.apply(idx)
            return False

        # ---- PYGAME rendering ---------------------------------------- #
        screen.fill((10, 5, 20))

        title_font = pygame.font.SysFont("monospace", 36)
        body_font  = pygame.font.SysFont("monospace", 20)
        btn_font   = pygame.font.SysFont("monospace", 22)

        title_surf = title_font.render(self.event.title, True, (220, 200, 100))
        screen.blit(title_surf, (self._btn_x, 40))

        self._render_wrapped(screen, body_font, self.event.description,
                             self._btn_x, self._desc_y, self._btn_w, 22)

        if not self.event.done:
            mouse_pos = pygame.mouse.get_pos()
            for i, opt in enumerate(self.event.options):
                btn_y = self._btn_y_start + i * self._btn_gap
                hovered = (self._btn_x < mouse_pos[0] < self._btn_x + self._btn_w and
                           btn_y < mouse_pos[1] < btn_y + self._btn_h)
                color = (80, 130, 80) if hovered else (50, 80, 50)
                pygame.draw.rect(screen, color,
                                 (self._btn_x, btn_y, self._btn_w, self._btn_h), 0, 6)
                pygame.draw.rect(screen, (120, 180, 120),
                                 (self._btn_x, btn_y, self._btn_w, self._btn_h), 2, 6)
                label = btn_font.render(opt.text, True, (230, 230, 230))
                screen.blit(label, (self._btn_x + 12, btn_y + 13))

                if hovered and opt.description:
                    tip = body_font.render(opt.description, True, (180, 180, 100))
                    screen.blit(tip, (self._btn_x + self._btn_w + 20, btn_y + 13))
        else:
            chosen_text = self.event.options[self.event.chosen_option].text
            msg = body_font.render(f"You chose: {chosen_text}", True, (180, 220, 180))
            screen.blit(msg, (self._btn_x, self._btn_y_start))
            cont = body_font.render("Click anywhere to continue.", True, (150, 150, 150))
            screen.blit(cont, (self._btn_x, self._btn_y_start + 35))

        return True

    def handle_event(self, event):
        if self.event is None or event.button != 1:
            return

        pos = pygame.mouse.get_pos()

        if self.event.done:
            return

        for i, opt in enumerate(self.event.options):
            btn_y = self._btn_y_start + i * self._btn_gap
            if (self._btn_x < pos[0] < self._btn_x + self._btn_w and
                    btn_y < pos[1] < btn_y + self._btn_h):
                self.event.apply(i)
                break

    # ------------------------------------------------------------------ #
    # Helper                                                               #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _render_wrapped(screen, font, text, x, y, max_width, line_height):
        words = text.split()
        line = ""
        dy = 0
        for word in words:
            test = (line + " " + word).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                screen.blit(font.render(line, True, (200, 200, 200)), (x, y + dy))
                dy += line_height
                line = word
        if line:
            screen.blit(font.render(line, True, (200, 200, 200)), (x, y + dy))
