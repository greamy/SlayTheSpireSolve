import pygame

from CombatSim.Actions.Listener import Listener
from CombatSim.Actions.Playable import Playable
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from enum import Enum


class Card(Playable):
    def __init__(self, name, card_type, energy, damage, attacks, block, draw, discard, exhaust, retain, player,
                 stance: Player.Stance = None, innate=False, temp_retain=False, id=-1):
        super().__init__(damage, attacks, block)
        self.name = name
        self.card_type = card_type
        self.energy = energy
        self.draw = draw
        self.discard = discard
        self.exhaust = exhaust
        self.retain = retain
        self.stance = stance
        self.upgraded = False
        self.innate = innate
        self.temp_retain = temp_retain
        self.playable = True
        self.description = ""
        self.id = id
        self.mantra = 0

        self.listener = None

        # Check for Master Reality listener - Upgrade if master reality has been played
        for listener in player.listeners:
            if Listener.Event.CARD_CREATED in listener.event_types:
                self.upgrade()

        # render attributes
        self.start_x = 50
        self.x = 50
        self.y = 450
        self.dist = 130
        self.width = 125
        self.height = 150

        self.text_embedding = None

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        if debug:
            print("Playing " + self.name + "...")
        player.draw_cards(self.draw, enemies, debug)

        if self.stance is not None:
            player.set_stance(self.stance)

    def upgrade(self):
        self.upgraded = True

    def is_power(self):
        return self.card_type == self.Type.POWER

    def is_skill(self):
        return self.card_type == self.Type.SKILL

    def is_attack(self):
        return self.card_type == self.Type.ATTACK

    def set_text_embedding(self, embedding):
        self.text_embedding = embedding

    def render(self, screen, font, pos, y=None, controller=None):
        if y is None:
            y = self.y
        self.x = self.start_x + (pos * self.dist)

        # Determine border color based on probability if available
        border_color = "white"
        if self.upgraded:
            border_color = 'green'

        # Override with probability-based color if RL agent is active
        if controller is not None and hasattr(controller, 'card_probabilities'):
            prob = controller.card_probabilities.get(pos, 0.0)

            # Dynamic color scaling based on min/max probabilities
            min_prob = getattr(controller, 'min_probability', 0.0)
            max_prob = getattr(controller, 'max_probability', 1.0)

            # Normalize probability to [0, 1] range based on current distribution
            if max_prob > min_prob:
                normalized_prob = (prob - min_prob) / (max_prob - min_prob)
            else:
                normalized_prob = 0.5  # If all probs are equal, use middle color

            # Calculate color gradient: green (high prob) to red (low prob)
            green = int(255 * normalized_prob)
            red = int(255 * (1 - normalized_prob))
            prob_color = (red, green, 0)

            # Use probability color for border (overrides upgrade color)
            border_color = prob_color

            # Render probability percentage above the card
            prob_text = f"{int(prob * 100)}%"
            prob_surface = font.render(prob_text, True, prob_color)
            screen.blit(prob_surface, (self.x + 10, y - 30))

        # Draw card border
        pygame.draw.rect(screen, border_color, pygame.Rect(self.x, y, self.width, self.height), 10, 2)

        # Draw card name
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.x+10, y+10))

        # Draw energy cost
        cost = font.render(str(self.energy), True, (0, 255, 0))
        screen.blit(cost, (self.x+(self.width - 20), y+10))

    def remove_listeners(self, player: Player):
        if self.listener is not None and self.listener in player.listeners:
            player.remove_listener(self.listener)

    def __str__(self):
        return self.name

    class Type(Enum):
        ATTACK = 0
        SKILL = 1
        POWER = 2
        STATUS = 3
