import random
import time

import pygame

from GameSim.Map.CombatRoom import CombatRoom
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, createEnemy, addCards

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    enemy = createEnemy("AcidSlimeSmall", 20, 1)
    # SET HEALTH HERE
    player = createPlayer(lib_path='CombatSim/Actions/Library', health=70, energy=3, gold=50,
                          potions=[], relics=[], cards=[])
    cards = ["Strike" for _ in range(4)]
    cards.extend(["Defend" for _ in range(4)])
    cards.extend(["Vigilance", "Eruption"])
    cards.extend(["Devotion" for _ in range(5)])
    cards.extend(["SandsofTime" for _ in range(2)])
    addCards(player, cards)

    combat = CombatRoom(player, [enemy], True)
    combat.start()

    # Open the map
    # let the player choose the next floor
    # player chooses up -> left = floor 2, room 3
    # mapgen.map[2][3] = Room

    # room.type == "E":

    renderer = Renderer(screen, combat)
    renderer.render_playable_combat()

def test():
    import pygame

    pygame.init()

    # Window setup
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cursor in Square Check")

    # Define the square's properties
    SQUARE_SIZE = 100
    square_x = (WINDOW_WIDTH - SQUARE_SIZE) // 2
    square_y = (WINDOW_HEIGHT - SQUARE_SIZE) // 2
    square_rect = pygame.Rect(square_x, square_y, SQUARE_SIZE, SQUARE_SIZE)

    # Colors
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    time_takens = []
    for i in range(5):
        running = True
        ct = 0
        start = time.time()
        while running and ct < 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get mouse position
            mouse_pos = random.randint(0, SQUARE_SIZE), random.randint(0, SQUARE_SIZE)

            # mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse is hovering over the square
            sub_square = pygame.Rect(square_x // 2, square_y // 2, SQUARE_SIZE, SQUARE_SIZE)
            if sub_square.collidepoint(mouse_pos):
                current_square_color = GREEN
            else:
                current_square_color = RED
            # sq_x = square_x // 2
            # sq_y = square_y // 2
            #
            # if sq_x < mouse_pos[0] < sq_x + SQUARE_SIZE and sq_y < mouse_pos[1] < sq_y + SQUARE_SIZE:
            #     current_square_color = GREEN
            # else:
            #     current_square_color = RED

            # Drawing
            screen.fill(WHITE)
            pygame.draw.rect(screen, current_square_color, square_rect)

            pygame.display.flip()
            ct += 1
        end = time.time()
        time_takens.append(end - start)
    print("time taken for 1000 checks: " + str(sum(time_takens) / len(time_takens)))
    pygame.quit()

if __name__ == "__main__":
    test()
