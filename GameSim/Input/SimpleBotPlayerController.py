import random

from CombatSim.Actions.Card import Card
from CombatSim.Entities.Player import Player
from GameSim.Input.Controller import PlayerController


class SimpleBotPlayerController(PlayerController):
    def __init__(self, delay=1):
        super().__init__()
        self.delay = delay
        self.counter = 0
        self.framerate = 60

    def get_target(self, player, enemies, playable, debug):
        # Find enemy in enemies with lowest health
        enemy = min(enemies, key=lambda x: x.health)
        return enemies.index(enemy), enemy

    def get_scry(self, player, enemies, cards, debug):
        # list of length cards of boolean values
        to_discard = set()

        for i in range(random.randint(0,len(cards))):
            choice = random.randint(0,len(cards)-1)
            to_discard.add(choice)
        to_discard = list(to_discard)
        return to_discard

    def get_max_dmg_possible(self, player, enemies, playable_cards):
        total_damage = 0
        for card in playable_cards:
            if card.damage > 0:
                total_damage += max([card.get_damage(player, enemy) for enemy in enemies])
        return total_damage

    def get_card_to_play(self, player, enemies, playable_cards, debug):
        _, ret = super().get_card_to_play(player, enemies, playable_cards, debug)
        if ret is None:
            return None, None
        if len(player.deck.hand) == 0:
            return None, None

        total_dmg_possible = self.get_max_dmg_possible(player, enemies, playable_cards)
        total_enemy_health = sum([enemy.health for enemy in enemies])

        # Enter Divinity if
        # 1. We are not in divinity
        # 2. we have enough mantra cards
        # 3. we can play all of them
        # 4. it makes sense to enter divinity
        if player.stance != Player.Stance.DIVINITY:
            mantra_cards = []
            mantra_possible = 0
            for i, card in enumerate(playable_cards):
                if card.mantra > 0:
                    # keep track of all cards which add mantra
                    mantra_possible += card.mantra
                    mantra_cards.append(card)

                    # if this new card in addition to all previous mantra cards found will allow us to enter divinity
                    # AND we have either:
                    # 1. 2 damage dealing cards to play with it
                    #             OR
                    # 2. we have lethal damage while in divinity
                    if mantra_possible + player.mantra >= 10 and sum(m.energy for m in mantra_cards) <= player.energy\
                            and (sum([1 if c.damage > 0 else 0 for c in playable_cards]) >= 2 or total_dmg_possible*3 > total_enemy_health):
                        return i, card

        # Enter Wrath if
        # 1. We aren't currently in wrath
        # 2. We have a card which lets us enter wrath
        # 3a. We have a card which enters another stance or exits stance which we have enough energy to play
        #               OR
        # 3b. We have a card which enters another stance next turn AND we won't take > 40% HP this turn from wrath damage
        #
        if player.stance != Player.Stance.WRATH:
            for i, card in enumerate(playable_cards):
                if card.stance == Player.Stance.WRATH:
                    energy_left = player.energy - card.energy
                    enemy_dmg = sum([enemy.intent.get_damage(enemy, player) for enemy in enemies])
                    other_stance_card = sum([1 if c.stance is not None and c.stance != Player.Stance.WRATH and c.energy <= energy_left else 0 for c in playable_cards + player.deck.draw_pile[:5]]) > 0
                    if other_stance_card and enemy_dmg <= player.health and enemy_dmg <= player.max_health * 0.4:
                        return i, card

        # Rule: Play any attack card that is lethal for an enemy.
        for enemy in enemies:
            highest_dmg_card = max(playable_cards, key=lambda x: x.get_damage(player, enemy))
            damage = highest_dmg_card.get_damage(player, enemy)
            if damage > enemy.health:
                return playable_cards.index(highest_dmg_card), highest_dmg_card

        # Rule: Exit wrath if we are in wrath and able to exit
        if player.stance == Player.Stance.WRATH:
            for i, card in enumerate(playable_cards):
                if card.stance is not None and card.stance != Player.Stance.WRATH:
                    return i, card

        # Rule: Play defense card if:
        #   1. Enemies are attacking for more than our current block
        #   2. We have a defense card in hand
        #
        total_enemy_dmg = 0
        for enemy in enemies:
            if enemy.intent.damage > 0:
                total_enemy_dmg += enemy.intent.get_damage(enemy, player)

        if total_enemy_dmg > player.block:
            biggest_block_card = max(playable_cards, key=lambda card: card.block)
            if biggest_block_card.block > 0:
                return playable_cards.index(biggest_block_card), biggest_block_card

        # If we dont need to block and cant kill,, try to play power
        for i, card in enumerate(playable_cards):
            if card.card_type == Card.Type.POWER:
                return i, card

        # Then finally play any attacks (that don't enter us into wrath)
        for enemy in enemies:
            highest_dmg_card = max(playable_cards, key=lambda x: x.get_damage(player, enemy))
            if highest_dmg_card.stance != Player.Stance.WRATH:
                return playable_cards.index(highest_dmg_card), highest_dmg_card

        # If all else fails, we play random card.
        index = random.randint(0, len(playable_cards) - 1)
        card = playable_cards[index]
        i = player.deck.hand.index(card)

        if len(enemies) == 0:
            return 0, card

        return i, card

    def get_map_choice(self, player, map_gen, floor, room_idx):
        self.counter += 1
        if self.counter % (self.framerate * self.delay) != 0:
            return None

        self.counter = 0
        avail_rooms = map_gen.get_avail_floors(floor, room_idx)
        return map_gen.map[floor][random.choice(avail_rooms)]