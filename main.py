from Deck import Deck
from Card import Card
from Player import Player
from Enemy import Enemy
from Combat import Combat
from Intent import Intent
from Stance import Stance


def main():
    my_cards = [Card(name="Strike"+str(i), cost=1, damage=6, attacks=1, block=0, types="attack", exhaust=False, status="none") for i in range(5)]
    my_cards.extend(Card(name="Defend"+str(i), cost=1, damage=0, attacks=0, block=5, types="skill", exhaust=False, status="none") for i in range(5))
    my_deck = Deck(my_cards)

    num_turns = []
    player_healths = []
    num_died = 0
    num_combat = 1
    for i in range(num_combat):
        Grants_ass = Player(health=69, block=0, status_list=[], energy=3, gold=690, potions=[], relics=[], deck=my_deck)
        jaw_worm = [Enemy(health=42, block=0, status_list=[], intent_set=[Intent(12, 1, 0, "", 25),
                                                                          Intent(7, 1, 5, "", 30),
                                                                          Intent(5, 1, 9, "", 45)])]
        combat = Combat(Grants_ass, jaw_worm)
        num_turn, player_health, is_alive = combat.start()
        num_turns.append(num_turn)
        player_healths.append(player_health)
        num_died += 0 if is_alive else 1


    print("The average number of turns for the combat is: " + str(sum(num_turns) / len(num_turns)) +
          "\nThe average remaining health of the player is: " + str(sum(player_healths) / len(player_healths)) +
          "\nThe player died " + str(num_died) + "/" + str(num_combat) + " times.")


if __name__ == "__main__":
    main()
