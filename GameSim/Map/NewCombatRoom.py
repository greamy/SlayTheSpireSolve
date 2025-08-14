import pygame

from CombatSim.Entities.Player import Player
from GameSim.Map.Room import Room
from GameSim.Render.Renderer import Renderer


class NewCombatRoom(Room):

    def __init__(self, player: Player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "N", floor, x, prev_rooms, next_rooms, act, ascension)
        self.counter = 0
        self.timer = 200

    def render_room(self, screen: pygame.Surface, screen_size, font, render_type):
        if render_type == Renderer.RenderType.NONE:
            return False
        if self.counter > self.timer:
            self.counter = 0
            return False

        self.font = pygame.font.SysFont("Arial", size=30)
        screen.fill("black")
        text = self.font.render("New Combat!", True, "white")
        screen.blit(text, (screen_size[0] // 2 - text.get_width() // 2, screen_size[1] // 2 - text.get_height() // 2))
        self.counter += 1
        return True
