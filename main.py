import pygame

from Combat import Combat
from CombatSim.Renderer import Renderer

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

    combat = Combat(player, [enemy], True)
    combat.start()

    # Open the map
    # let the player choose the next floor
    # player chooses up -> left = floor 2, room 3
    # mapgen.map[2][3] = Room

    # room.type == "E":



    renderer = Renderer(screen, combat)
    renderer.render_playable_combat()

if __name__ == "__main__":
    main()
