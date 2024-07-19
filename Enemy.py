from Entity import Entity
import random


class Enemy(Entity):
    def __init__(self, health, block, status_list, intent_set):
        super().__init__(health, block, status_list)
        self.intent = 0

        total_prob = sum([intent.probability for intent in intent_set])
        if total_prob != 100:
            print("Invalid probabilities. Must add to 100 percent!")
        self.intent_set = sorted(intent_set, key=lambda x: x.probability, reverse=False)

    def do_turn(self, player):
        current_prob = 0
        choice = random.randint(0, 100)
        for intent in self.intent_set:
            if choice < (intent.probability + current_prob):
                intent.play(self, player)
                return
            current_prob += intent.probability


    def __str__(self):
        return "ENEMY\nHealth: " + str(self.health) + " Block: " + str(self.block)


