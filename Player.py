from Entity import Entity
from Deck import Deck
from Stance import Stance
import random


class Player(Entity):
    def __init__(self, health: int, block: int, status_list: list, energy: int,
                 gold: int, potions: list, relics: list, deck: Deck):
        super().__init__(health, block, status_list)
        self.energy = energy
        self.gold = gold
        self.status_list = status_list
        self.potions = potions
        self.relics = relics
        self.deck = deck
        self.draw_amount = 5
        self.max_energy = 3
        self.stance = Stance.NONE

    def start_turn(self):
        super().start_turn()
        self.energy = self.max_energy
        self.draw_cards(self.draw_amount)

    def do_turn(self, enemies):
        # TODO: Make player play potions
        while self.energy > 0:
            success = self.play_card(random.choice(self.deck.hand), enemies[0])
            if not success:
                for card in self.deck.hand:
                    if card.energy <= self.energy:
                        success = self.play_card(card, enemies[0])
                        break

            if not success:
                break
            else:
                for enemy in enemies:
                    if not enemy.is_alive():
                        enemies.remove(enemy)
                if len(enemies) == 0:
                    return

        self.deck.end_turn()
        if self.stance == Stance.DIVINITY:
            self.set_stance(Stance.NONE)

    def take_damage(self, damage):
        if self.stance == Stance.WRATH:
            damage *= 2
        super().take_damage(damage)


    def draw_cards(self, amount):
        self.deck.draw_cards(amount)

    def play_card(self, card, enemy):
        if card not in self.deck.hand:
            print("Played card does not exist in hand")
            return False
        if card.energy > self.energy:
            print("Played card costs too much energy!")
            return False
        self.energy -= card.energy
        card.play(self, enemy)
        self.deck.discard(self.deck.hand.index(card))
        return True

    def gain_block(self, amount):
        self.block += amount

    def use_potion(self, potion):
        pass

    def set_stance(self, stance: Stance):
        if self.stance == Stance.CALM and stance != Stance.CALM:
            self.energy += 2
        if self.stance == Stance.WRATH and stance != Stance.WRATH:
            self.damage_dealt_multiplier /= 2
        if self.stance == Stance.DIVINITY and stance != Stance.DIVINITY:
            self.damage_dealt_multiplier /= 3

        if self.stance != Stance.WRATH and stance == Stance.WRATH:
            self.damage_dealt_multiplier *= 2
        if self.stance != Stance.DIVINITY and stance == Stance.DIVINITY:
            self.damage_dealt_multiplier *= 3
            self.energy += 3

        self.stance = stance

    def begin_combat(self):
        # TODO: Ensure all cards are in the draw pile, not in discard or exhaust
        self.deck.begin_combat()
        self.deck.shuffle()

    def __str__(self):
        return "PLAYER\nHealth: " + str(self.health) + "\nBlock: " + str(self.block) + "\n Deck: " + str(self.deck)
