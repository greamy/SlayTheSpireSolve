from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Entity import Entity
import random
import pygame

class Enemy(Entity):
    def __init__(self, health, intent_set, ascension, minion=False):
        super().__init__(health, x=500)

        total_prob = sum([intent.probability for intent in intent_set])
        if total_prob != 100:
            raise ValueError("Invalid probabilities. Must add to 100 percent!")
        self.intent_set = sorted(intent_set, key=lambda x: x.probability, reverse=False)
        self.intent = None
        self.last_intent = None
        self.num_consecutive = 1
        self.num_turns = 0
        self.choose_intent()
        self.minion = minion
        self.mark = 0
        self.ascension = ascension

    def start_turn(self, opponents, debug):
        super().start_turn(opponents, debug)
        self.notify_listeners(Listener.Event.START_TURN, opponents[0], [self], debug)

    def end_turn(self, opponents, debug):
        super().end_turn(opponents, debug)
        self.notify_listeners(Listener.Event.END_TURN, opponents[0], [self], debug)

    def gain_block(self, amount, opponents, debug):
        super().gain_block(amount, opponents, debug)
        self.notify_listeners(Listener.Event.BLOCK_GAINED, opponents[0], [self], debug)

    def choose_intent(self):
        current_prob = 0
        choice = random.randint(0, 99)
        self.intent = None
        for intent in self.intent_set:
            if intent == self.last_intent:
                self.num_consecutive += 1
            if choice < (intent.probability + current_prob) and self.is_valid_intent(intent):
                self.intent = intent
                break
            else:
                self.num_consecutive -= 1
            current_prob += intent.probability
        if self.intent is None:
            self.choose_intent()
        self.last_intent = self.intent

    def is_valid_intent(self, intent: Intent) -> bool:
        pass

    def do_turn(self, player, debug):
        self.intent.play(self, [self], player, [player], debug)
        self.num_turns += 1
        self.choose_intent()

        self.end_turn([player], debug)

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, "red", (self.x, self.y, self.width, self.height), 50, 5)

        intent_str = ["INTENT: " + self.intent.name, str(self.intent.damage) + " * " + str(self.intent.attacks) + " dmg",
                      str(self.intent.block) + " block"]
        lines = []
        for line in intent_str:
            lines.append(self.font.render(line, True, self.intent.color))

        for i, line in enumerate(lines):
            screen.blit(line, (self.x + self.width+5, self.y + (i-1) * (self.text_size + 5)))


    def __str__(self):
        return "ENEMY\nHealth: " + str(self.health) + " Block: " + str(self.block)


