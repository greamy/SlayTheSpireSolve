from enum import Enum

import pygame

from GameSim.Map.Room import Room


class RestRoom(Room):
    class Actions(Enum):
        REST = 0
        UPGRADE = 1
        UPGRADED = 2
        RECALL = 3
        TOKE = 4
        DONE = 5

    MAX_HP_FACTOR = 0.3

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "R", floor, x, prev_rooms, next_rooms, act, ascension)

        self.action = None
        self.upgraded_card = None

        # render attributes
        self.color = (20, 255, 20) # Green
        self.counter = 1

        self.btn_width = 250
        self.btn_height = 150

        self.rest_btn_x = 250
        self.rest_btn_y = 200
        self.rest_btn_color = "green"

        self.upgrade_btn_x = 550
        self.upgrade_btn_y = 200
        self.upgrade_color = "orange"

        self.title_text_x = 600
        self.title_text_y = 10

        self.card_start_y = 50
        self.card_spacing = 175

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font, render_type):
        img = pygame.image.load("../images/Rooms/campfire.png")
        img = pygame.transform.scale(img, screen_size, screen)
        if self.action is None:
            # Player must choose what to do at rest site.
            title = font.render("Time for a Break", True, 'white')
            screen.blit(title, (self.title_text_x, self.title_text_y))

            pygame.draw.rect(screen, self.rest_btn_color, (self.rest_btn_x, self.rest_btn_y, self.btn_width, self.btn_height))
            rest_txt = font.render("Rest", True, "Black")
            screen.blit(rest_txt, (self.rest_btn_x + 20, self.rest_btn_y + 20))
            pygame.draw.rect(screen, self.upgrade_color, (self.upgrade_btn_x, self.upgrade_btn_y, self.btn_width, self.btn_height))
            upgrade_txt = font.render("Upgrade", True, "Black")
            screen.blit(upgrade_txt, (self.upgrade_btn_x + 20, self.upgrade_btn_y + 20))
        elif self.action == self.Actions.REST:
            # Player chose to rest, add health and exit rest site.
            self.player.do_rest()
            return False

        elif self.action == self.Actions.UPGRADE:
            # Player chose to upgrade. Display all cards in deck and allow choice of upgrade.
            title = font.render("Upgrade a Card.", True, 'white')
            screen.blit(title, (self.title_text_x, self.title_text_y))
            for i, card in enumerate(self.player.deck.draw_pile):
                if not card.upgraded:
                    card.render(screen, font, i % 8, self.card_start_y + (i // 8) * self.card_spacing)

        elif self.action == self.Actions.UPGRADED:
            title = font.render("Upgrade Complete", True, 'white')
            screen.blit(title, (self.title_text_x, self.title_text_y))
            # Player chose a card to upgrade. render this card until they click anywhere.
            self.upgraded_card.render(screen, font, 4, 200)

        elif self.action == self.Actions.DONE:
            return False

        return True


    def handle_event(self, event):
        if event.button == 1:

            # get position of mouse click
            pos = pygame.mouse.get_pos()
            if self.action is None:
                if self.rest_btn_x < pos[0] < self.rest_btn_x + self.btn_width and self.rest_btn_y < pos[1] < self.rest_btn_y + self.btn_height:
                    self.action = self.Actions.REST
                elif self.upgrade_btn_x < pos[0] < self.upgrade_btn_x + self.btn_width and self.upgrade_btn_y < pos[1] < self.upgrade_btn_y + self.btn_height:
                    self.action = self.Actions.UPGRADE

            elif self.action == self.Actions.UPGRADE:
                for i, card in enumerate(self.player.deck.draw_pile):
                    y = self.card_start_y + (i // 8) * self.card_spacing
                    if card.x < pos[0] < card.x + card.width and y < pos[1] < y + card.height:
                        card.upgrade()
                        self.upgraded_card = card
                        self.action = self.Actions.UPGRADED
                        break
            elif self.action == self.Actions.UPGRADED:
                self.action = self.Actions.DONE
