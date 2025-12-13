import time

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

        # Enemy turn delay mechanism
        self.enemy_turn_counter = 0
        self.enemy_turn_ready = False

    def start(self):
        self.enemies = self.create_enemies(self.act, self.ascension)
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.controller.begin_combat(self.player, self.enemies, self.debug)
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
                self.player.end_turn(self.enemies, self.debug)
                self.current_turn = self.ENEMY_TURN
                # Reset enemy turn delay counter when switching to enemy turn
                self.enemy_turn_counter = 0
                self.enemy_turn_ready = False

        elif self.current_turn == self.ENEMY_TURN:
            # Add delay before enemy turn executes (similar to player's wait_for_counter)
            if not self.enemy_turn_ready:
                self.enemy_turn_counter += 1
                delay = self.player.controller.delay
                framerate = self.player.controller.framerate
                if delay != 0 and self.enemy_turn_counter < (delay * framerate):
                    return True  # Keep waiting, don't execute enemy turn yet
                self.enemy_turn_ready = True

            # Execute enemy turn after delay has passed
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
            self.player.end_combat(self.enemies, self.debug)
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

        self.player.end_combat(self.debug)
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

            # Render end turn probability if available (RL agent in PYGAME mode)
            if hasattr(self.player, 'controller') and self.player.controller is not None and hasattr(self.player.controller, 'end_turn_probability'):
                end_turn_prob = self.player.controller.end_turn_probability
                controller = self.player.controller

                # Dynamic color scaling based on min/max probabilities
                min_prob = getattr(controller, 'min_probability', 0.0)
                max_prob = getattr(controller, 'max_probability', 1.0)

                # Normalize probability to [0, 1] range based on current distribution
                if max_prob > min_prob:
                    normalized_prob = (end_turn_prob - min_prob) / (max_prob - min_prob)
                else:
                    normalized_prob = 0.5  # If all probs are equal, use middle color

                # Calculate color gradient: green (high prob) to red (low prob)
                green = int(255 * normalized_prob)
                red = int(255 * (1 - normalized_prob))
                color = (red, green, 0)

                # Render probability percentage above the End Turn button
                prob_text = f"{int(end_turn_prob * 100)}%"
                prob_surface = main_font.render(prob_text, True, color)
                screen.blit(prob_surface, (self.end_turn_x + 10, self.end_turn_y - 30))

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
