from POMDPSolve.FirstTurnSolver import FirstTurnSolver


def main():

    cards = {
        "Strike": [4, 0.6],
        "Defend": [4, 2.5],
        "Eruption": [1, 0.9],
        "Vigilance": [1, 4.0]
    }
    hand_solver = FirstTurnSolver(cards, 5)
    expectation = hand_solver.solve()
    print(expectation)
    print(len(hand_solver.possible_hands))
    # would saving the list off all possible 4 card hands be equivalent to all possible action 2 hands?


if __name__ == "__main__":
    main()