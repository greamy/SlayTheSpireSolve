from Actions.Card import Card
from Entities.Player import Player
from Entities.Enemy import Enemy
from Combat import Combat
from Actions.Intent import Intent
import copy
import os
import importlib
import time


def main():
    my_cards = [Card(name="Strike" + str(i), energy=1, damage=6, attacks=1, block=0, draw=0, discard=0, exhaust=False,
                     status="none", stance=None) for i in range(5)]
    my_cards.extend(
        Card(name="Defend" + str(i), energy=1, damage=0, attacks=0, block=5, draw=0, discard=0, exhaust=False,
             status="none", stance=None) for i in range(5))
    my_cards.append(Card("Eruption", 2, 9, 1, 0, 0, 0, False,
                         "", stance=Player.Stance.WRATH))
    my_cards.append(Card("Vigilance", 2, 0, 0, 8, 0, 0, False,
                         "", stance=Player.Stance.CALM))

    card_name_list = os.listdir(os.path.join(os.curdir, "./Actions/Library"))
    for card_name in card_name_list:
        if card_name.endswith(".py"):
            card_name = card_name[:-3]
            module = importlib.import_module("Actions.Library." + card_name)
            class_ = getattr(module, card_name)
            my_cards.append(class_())

    num_turns = []
    player_healths = []
    num_died = 0
    num_combat = 10000
    start = time.time()
    for i in range(num_combat):
        grants_ass = Player(health=69, status_list=[], energy=3, gold=690, potions=[], relics=[],
                            cards=copy.deepcopy(my_cards))
        jaw_worm = Enemy(health=42, status_list=[], intent_set=[Intent(12, 1, 0, "", 25),
                                                                         Intent(7, 1, 5, "", 30),
                                                                         Intent(5, 1, 9, "", 45)])
        combat = Combat(grants_ass, [jaw_worm], False)
        num_turn, player_health, is_alive = combat.start()
        num_turns.append(num_turn)
        player_healths.append(player_health)
        num_died += 0 if is_alive else 1

    end = time.time()
    print("The average number of turns for the combat is: " + str(sum(num_turns) / len(num_turns)) +
          "\nThe average remaining health of the player is: " + str(sum(player_healths) / len(player_healths)) +
          "\nThe player died " + str(num_died) + "/" + str(num_combat) + " times.")
    print("Program ran in "  + str(end - start) + " seconds.")


if __name__ == "__main__":
    main()
