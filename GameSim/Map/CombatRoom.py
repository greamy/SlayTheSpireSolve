import pygame

from CombatSim.Entities.Enemy import Enemy
from GameSim.Map.Room import Room
from GameSim.Render.Renderer import Renderer


class CombatRoom(Room):
    PLAYER_TURN = 0
    ENEMY_TURN = 1

    def __init__(self, player, type, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, type, floor, x, prev_rooms, next_rooms, act, ascension)
        self.current_turn = self.PLAYER_TURN
        self.player_won = None

        self.enemies = None
        self.debug = False
        self.start_card = None
        # self.state = CombatState(self.player, self.enemies)

        # render attributes
        self.end_turn_x = 525
        self.end_turn_y = 300
        self.end_turn_width = 160
        self.end_turn_height = 80

        self.fail_msg = None
        self.fail_msg_counter = 0

    def start(self):
        self.enemies = self.create_enemies(self.act, self.ascension)
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        # return self.run()

    def create_enemies(self, act, ascension) -> list[Enemy]:
        pass

    def end_combat(self):
        pass

    def get_total_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def do_next_turn(self):
        start_player = False
        if self.current_turn == self.PLAYER_TURN:
            turn_over = self.player.do_next_action(self.enemies, self.debug)
            if turn_over:
                self.current_turn = self.ENEMY_TURN

        elif self.current_turn == self.ENEMY_TURN:
            for enemy in self.enemies:
                enemy.start_turn([self.player], self.debug)
                enemy.do_turn(self.player, self.debug)
            self.current_turn = self.PLAYER_TURN
            start_player = True

        if self.player.health > 0 and self.get_total_enemy_health() > 0:
            if start_player:
                self.player.start_turn(self.enemies, self.debug)
            return True
        else:
            if self.player.health > 0:
                self.player_won = False
            else:
                self.player_won = False
            self.player.end_combat()
            self.end_combat()
            return False


    def run(self):
        # Game loop of player turn -> Enemy turn until enemies or player is killed.
        num_turns = 0
        while self.player.health > 0 and self.get_total_enemy_health() > 0:
            self.player.start_turn(self.enemies, self.debug)
            self.player.do_turn(self.enemies, self.debug)


            for enemy in self.enemies:
                enemy.start_turn([self.player], self.debug)
                enemy.do_turn(self.player, self.debug)

            if self.debug:
                print(self.player)
                for enemy in self.enemies:
                    print(enemy)

            num_turns += 1

        self.player.end_combat()
        if self.debug:
            if self.player.health <= 0:
                print("YOU LOSE")
            if self.get_total_enemy_health() <= 0:
                print("YOU WIN")

        return num_turns, self.player.health, self.player.is_alive()

    def get_state(self):
        return self.state.get_state()

    def run_turn(self, card_to_play, target_enemy):
        total_enemy_health = self.get_total_enemy_health()
        player_health = self.player.health

        self.player.play_card(card_to_play, target_enemy, self.enemies, self.debug)
        # if not success:
        #     return None, None
        playable_cards = self.player.get_playable_cards()

        reward = 0
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)
                reward += 10
        if self.get_total_enemy_health() <= 0:
            reward += 10
        elif self.player.energy <= 0 or len(playable_cards) == 0:
            self.player.end_turn(self.enemies, self.debug)

            for enemy in self.enemies:
                enemy.start_turn([self.player], self.debug)
                enemy.do_turn(self.player, self.debug)

            if self.player.health <= 0:
                reward -= 20
            else:
                self.player.start_turn(self.enemies, self.debug)

        new_enemy_health = self.get_total_enemy_health()
        new_player_health = self.player.health

        # receive reward equal to damage done to enemies minus damage taken to health.
        # +10 for killing enemy
        # -20 for dying
        reward = reward + total_enemy_health-new_enemy_health - (player_health - new_player_health)
        if self.player.is_alive() and self.get_total_enemy_health() >= 0:
            return self.get_state(), reward
        else:
            return None, reward

    def render_room(self, screen, screen_size, main_font, render_type):
        if render_type == Renderer.RenderType.PYGAME:
            pos = pygame.mouse.get_pos()
            # check if any card was hovered
            help_box_x = 50
            help_box_y = 260
            help_box_width = 325
            help_box_height = 175
            card_hovered = None
            for card in self.player.deck.hand:
                if card.x < pos[0] < card.x + card.width and card.y < pos[1] < card.y + card.height:
                    # show info about the card
                    card_hovered = card

            screen.fill((0, 0, 0))  # SCREEN CLEARING IS HAPPENING HERE!!! BE CAREFUL

            title_font = pygame.font.SysFont("monospace", 40)
            self.player.render(screen, main_font)

            for enemy in self.enemies:
                enemy.render(screen, main_font)

            if self.player_won is None:
                if self.current_turn == self.PLAYER_TURN:
                    text = title_font.render("PLAYER TURN", True, (100, 100, 255))
                else:
                    text = title_font.render("ENEMY TURN", True, (255, 100, 100))
                screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))
            else:  # if game is over
                if self.player_won:
                    text = title_font.render("WINNER WINNER CHICKEN DINNER", True, (255, 255, 255))
                    screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))
                else:
                    text = title_font.render("no chicken :(", True, (255, 255, 255))
                    screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))

            if card_hovered is not None:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (help_box_x, help_box_y, help_box_width, help_box_height),
                                 0, 2)
                name = main_font.render(card_hovered.name, True, (0, 0, 0))
                screen.blit(name, (help_box_x + 5, help_box_y + 10))
                cost = main_font.render("Energy: " + str(card_hovered.energy), True, (0, 255, 0))
                screen.blit(cost, (help_box_x + help_box_width - 125, help_box_y + 10))

                # separate description into 20 characters per line
                description_lines = []
                description_text = card_hovered.description
                while len(description_text) > 25:
                    line = description_text[:25]
                    description_lines.append(line)
                    description_text = description_text[25:]
                description_lines.append(description_text)

                for i, line in enumerate(description_lines):
                    text = main_font.render(line, True, (255, 100, 50))
                    screen.blit(text, (help_box_x + 5, help_box_y + 30 + (i * 20)))

            pygame.draw.rect(screen, (100, 175, 100),
                             (self.end_turn_x, self.end_turn_y, self.end_turn_width, self.end_turn_height), 0, 5)
            title_font = pygame.font.SysFont("monospace", 30)
            end_turn_text = title_font.render("End Turn", True, (0, 0, 0))
            screen.blit(end_turn_text, (self.end_turn_x + 5, self.end_turn_y + 5))

        combat_running = self.do_next_turn()
        return combat_running

    def handle_event(self, event):
        if event.button == 1 and self.current_turn == self.PLAYER_TURN:
            # get position of mouse click
            pos = pygame.mouse.get_pos()

            if self.end_turn_x < pos[0] < self.end_turn_x + self.end_turn_width and \
                    self.end_turn_y < pos[1] < self.end_turn_y + self.end_turn_height:
                self.player.turn_over = True
            else:
                self.player.controller.handle_event(pos, self.player, self.enemies)
