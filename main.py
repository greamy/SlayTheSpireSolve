import importlib
import os

from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from Combat import Combat
from CombatSim.Actions.Intent import Intent
import time


def get_cards(player: Player):
    my_cards = []
    card_name_list = os.listdir(os.path.join(os.curdir, "./CombatSim/Actions/Library"))
    for card_name in card_name_list:
        if card_name != "Expunger.py" and card_name.endswith(".py"):
            card_name = card_name[:-3]
            module = importlib.import_module("CombatSim.Actions.Library." + card_name)
            class_ = getattr(module, card_name)
            my_cards.append(class_(player))

    return my_cards

def main():
    # my_cards = [Card(name="Strike" + str(i), card_type=Card.Type.ATTACK, energy=1, damage=6, attacks=1, block=0, draw=0, discard=0, retain=False, exhaust=False,
    #                  status="", stance=None) for i in range(5)]
    # my_cards.extend(
    #     Card(name="Defend" + str(i), card_type=Card.Type.SKILL, energy=1, damage=0, attacks=0, block=5, draw=0, discard=0, retain=False, exhaust=False,
    #          status="", stance=None) for i in range(5))
    # my_cards.append(Card("Eruption", Card.Type.ATTACK, 2, 9, 1, 0, 0, 0, False,False,
    #                      "", stance=Player.Stance.WRATH))
    # my_cards.append(Card("Vigilance", Card.Type.SKILL,2, 0, 0, 8, 0, 0, False, False,
    #                      "", stance=Player.Stance.CALM))

    my_cards = []

    num_turns = []
    player_healths = []
    num_died = 0
    num_combat = 10000
    start = time.time()
    for i in range(num_combat):
        grants_ass = Player(health=69, energy=3, gold=690, potions=[], relics=[],
                            cards=[])
        grants_ass.deck = Player.Deck(get_cards(grants_ass))
        # jaw_worm = Enemy(health=51, status_list=[], intent_set=[Intent(12, 1, 0, 25),
        #                                                                  Intent(7, 1, 5, 30),
        #                                                                  Intent(5, 1, 9, 45)])
        jaw_worm = JawWorm(20)
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
