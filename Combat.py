import random

import numpy as np
import pygame

from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from QBot.Environments.States.CombatState import CombatState


class Combat:
    PLAYER_TURN = 0
    ENEMY_TURN = 1

    def __init__(self, player: Player, enemies: list[Enemy], debug: bool):
        self.player = player
        self.current_turn = self.PLAYER_TURN
        self.player_won = None
        if len(enemies) < 1:
            print("No enemies in combat")

        self.enemies = enemies
        self.debug = debug
        self.start_card = None
        self.state = CombatState(self.player, self.enemies)

    def start(self):
        self.player.begin_combat(self.enemies, self.debug)
        # return self.run()

    def get_total_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def do_next_turn(self):
        if self.current_turn == self.PLAYER_TURN:
            turn_over = self.player.do_next_action(self.enemies, self.debug)
            if turn_over:
                self.current_turn = self.ENEMY_TURN

        elif self.current_turn == self.ENEMY_TURN:
            for enemy in self.enemies:
                enemy.start_turn([self.player], self.debug)
                enemy.do_turn(self.player, self.debug)
            self.current_turn = self.PLAYER_TURN
            self.player.start_turn(self.enemies, self.debug)

        if self.player.health > 0 and self.get_total_enemy_health() > 0:
            return True
        else:
            if self.player.health > 0:
                self.player_won = True
            else:
                self.player_won = False
            return False

    def renderall(self, screen):
        self.player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)
        font = pygame.font.SysFont("monospace", 20)
        if self.player_won is not None:
            if self.player_won :

                text = font.render("WINNER WINNER CHICKEN DINNER", True, (255, 255, 255))
                screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))
            else:
                text = font.render("no chicken :(", True, (255, 255, 255))
                screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 10))

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

