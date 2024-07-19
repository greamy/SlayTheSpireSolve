from Entity import Entity


class Player(Entity):
    def __init__(self, health, block, status_list, energy, gold, potions, relics, deck):
        super().__init__(health, block, status_list)
        self.energy = energy
        self.gold = gold
        self.status_list = status_list
        self.potions = potions
        self.relics = relics
        self.deck = deck

    def play_card(self, card):
        self.energy -= card.energy
        my_deck.discard(card) #The discard function takes an index...., so we should decide on what to do about that


    def gain_block(self, amount):
        self.block += amount

    def use_potion(self, potion):
        pass

    def __str__(self):
        return self.label
