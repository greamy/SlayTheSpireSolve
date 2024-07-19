from Deck import Deck
from Card import Card
from Player import Player


def main():
    my_cards = [Card(name="Strike"+str(i), cost=1, damage=6, attacks=1, block=0, types="attack", exhaust=False, status="none") for i in range(5)]
    my_cards.extend(Card(name="Defend"+str(i), cost=1, damage=0, attacks=0, block=5, types="skill", exhaust=False, status="none") for i in range(5))
    my_deck = Deck(my_cards)

    Grants_ass = [Player(health=69, block=0, status_list=0, energy=3, gold=690, potions=0, relics=0, deck=my_deck)]

    my_deck.shuffle()
    print(my_deck)

    my_deck.draw_hand(5)
    print(my_deck)

    my_deck.draw(2)
    print(my_deck)
    my_deck.discard(6)
    my_deck.end_turn()
    print(my_deck)
    card.play(1)
    print(my_deck)
if __name__ == "__main__":
    main()


