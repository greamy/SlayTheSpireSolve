from CombatSim.Actions.Intent import Intent
from CombatSim.Entities.Entity import Entity
import random


class Enemy(Entity):
    def __init__(self, health, intent_set, ascension, minion=False):
        super().__init__(health)

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

    def __str__(self):
        return "ENEMY\nHealth: " + str(self.health) + " Block: " + str(self.block)


