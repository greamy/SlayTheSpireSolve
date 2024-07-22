from Entities.Entity import Entity
import random


class Enemy(Entity):
    def __init__(self, health, status_list, intent_set):
        super().__init__(health, status_list)

        total_prob = sum([intent.probability for intent in intent_set])
        if total_prob != 100:
            raise ValueError("Invalid probabilities. Must add to 100 percent!")
        self.intent_set = sorted(intent_set, key=lambda x: x.probability, reverse=False)
        self.intent = None
        self.choose_intent()

    def choose_intent(self):
        current_prob = 0
        choice = random.randint(0, 99)
        for intent in self.intent_set:
            if choice < (intent.probability + current_prob):
                self.intent = intent
                break
            current_prob += intent.probability

    def do_turn(self, player, debug):
        self.intent.play(self, player, [player], debug)
        self.choose_intent()


    def __str__(self):
        return "ENEMY\nHealth: " + str(self.health) + " Block: " + str(self.block)


