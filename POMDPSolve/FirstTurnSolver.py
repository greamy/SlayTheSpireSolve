
class FirstTurnSolver:
    def __init__(self, cards: dict, num_draw=5):
        self.cards = cards
        self.num_draw = num_draw
        self.hand_generator = self.HandGenerator(cards, max_draw=num_draw)
        self.possible_hands = self.hand_generator.solve() # list of all possible hands based on cards dictionary
        print(self.possible_hands)

    def solve(self):
        # self.cards is a dictionary like this:
        # key: card name
        # value: list, [num_in_deck, reward(s)]]
        all_expected = []
        for hand in self.possible_hands[-1]:
            all_expected.append(self.solve_hand(hand, 3, 0, ""))
        return (sum(all_expected) / len(all_expected))

    def solve_hand(self, hand, energy, block, stance):
        if energy == 0:
            return -6 + min(6, 9.5 * block) # cant gain from more than 12 block
        playable_cards = [card for card in hand if not (energy < 2 and card in ["Eruption", "Vigilance"])]
        if len(playable_cards) == 0:
            return -6 + min(6, 9.5 * block) # cant gain from more than 12 block
        counts = {}
        for card in playable_cards:
            if card in counts:
                counts[card] += 1
            else:
                counts[card] = 1
        probs = {}

        for card, count in counts.items(): # all key, value pairs in the dictionary
            if stance == "W" and card == "Strike":
                card += "W"

            probs[card] = count / self.num_draw
        # ohh shoot defends have a list of rewards
        future_expected = 0
        for card in hand:
            cost = 1
            stance = ""
            if card == "Vigilance":
                stance = "C"
                cost = 2
            if card == "Eruption":
                stance = "E"
                cost = 2

            future_expected += self.solve_hand([c for c in hand if c != card], self.cards[card][2] + block, energy - cost, stance)
        future_expected /= len(hand)
        return sum([prob * self.cards[card][1] for card, prob in probs.items()]) + future_expected

    class HandGenerator:
        def __init__(self, cards, max_draw):
            """
            Initializes the HandGenerator.

            Args:
                cards (dict): A dictionary where keys are card names and values are
                              lists like [num_in_deck, reward(s)].
                max_draw (int): The maximum number of cards allowed in a hand.
            """

            self.cards = cards
            self.max_draw = max_draw

            self.card_names = list(self.cards.keys())
            self.all_hands = []

        def solve(self):
            """
            Generates all possible hands and returns them as a list of lists.
            """
            self.all_hands = []
            # We start the recursive generation with an empty hand and from the first card type
            self._generate_hands_recursive([], 0)

            new_hands = [[hand for hand in self.all_hands if len(hand) ==  j] for j in range(5)]
            self.all_hands = new_hands

            print(self.all_hands)
            return self.all_hands

        def _generate_hands_recursive(self, current_hand, start_index):
            """
            A private helper method that recursively finds all valid hands.

            Args:
                current_hand (list): The hand built so far in this path of the recursion.
                start_index (int): The index in self.card_names to start considering
                                   cards from. This prevents duplicate combinations
                                   (e.g., ['A', 'B'] and ['B', 'A']).
            """
            # Base Case: If the hand is full, we can't add any more cards.
            if len(current_hand) == self.max_draw:
                return

            # Recursive Step: Iterate through available card types to add one.
            for i in range(start_index, len(self.card_names)):
                card_name = self.card_names[i]
                max_allowed = self.cards[card_name][0]

                # Constraint Check: Can we add another copy of this card?
                # Check how many times this card is already in our current hand.
                if current_hand.count(card_name) < max_allowed:
                    # 1. Choose: Add the new card to the hand.
                    current_hand.append(card_name)

                    # Add the newly formed hand to our results list.
                    # We add a copy to prevent it from being modified by later steps.
                    self.all_hands.append(list(current_hand))

                    # 2. Explore: Recurse to find all hands that can be built from this new hand.
                    # We pass 'i' as the new start_index (not i + 1) to allow for
                    # adding more copies of the same card (e.g., ['A', 'A']).
                    self._generate_hands_recursive(current_hand, i)

                    # 3. Unchoose (Backtrack): Remove the card to explore other possibilities.
                    # This is the crucial step. After exploring all hands starting
                    # with ['A', 'B'], we pop 'B' to then explore hands starting
                    # with ['A', 'C'], for example.
                    current_hand.pop()

