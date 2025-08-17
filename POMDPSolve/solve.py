from POMDPSolve.FirstTurnSolver import FirstTurnSolver


def main():

    cards = {
        "Strike": [4, 0.6, 0],
        "Defend": [4, 0, 5],
        "Eruption": [1, 0.9, 0],
        "Vigilance": [1, 0, 8]
    }
    hand_solver = FirstTurnSolver(cards, 5)
    expectation = hand_solver.solve()
    print(expectation)
    print(len(hand_solver.possible_hands))
    # would saving the list off all possible 4 card hands be equivalent to all possible action 2 hands?


if __name__ == "__main__":
    main()