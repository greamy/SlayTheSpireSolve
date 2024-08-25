import importlib
import os

from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from Combat import Combat
from CombatSim.Actions.Intent import Intent
import time


def main():
    num_turns = []
    player_healths = []
    num_died = 0
    num_combat = 10000
    start = time.time()
    for i in range(num_combat):
        cards = list(Player.get_implemented_cards("CombatSim/Actions/Library").keys())
        cards.remove("Expunger")
        grants_ass = Player(health=69, energy=3, gold=690, potions=[], relics=[],
                            cards=cards)
        jaw_worm = JawWorm(0, 1)
        combat = Combat(grants_ass, [jaw_worm], False)
        num_turn, player_health, is_alive = combat.start()
        num_turns.append(num_turn)
        player_healths.append(player_health)
        num_died += 0 if is_alive else 1

    end = time.time()
    print("The average number of turns for the combat is: " + str(sum(num_turns) / len(num_turns)) +
          "\nThe average remaining health of the player is: " + str(sum(player_healths) / num_combat) +
          "\nThe player died " + str(num_died) + "/" + str(num_combat) + " times.")
    print("Program ran in " + str(end - start) + " seconds.")
    print("The best combat had the player end at " + str(max(player_healths)) + " health with a "
          + str((player_healths.count(max(player_healths)) / num_combat) * 100) + " % chance.")
    print("The worst combat had the player end at " + str(min(player_healths)) + " health with a "
          + str((player_healths.count(min(player_healths)) / num_combat) * 100) + " % chance.")


if __name__ == "__main__":
    main()
