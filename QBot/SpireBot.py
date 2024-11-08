import copy
import importlib
import random
import time

from spirecomm.communication.action import *
from spirecomm.spire.game import Game
import spirecomm.spire.character as char

from Combat import Combat
from CombatSim.Entities.Player import Player


class SpireBot:
    def __init__(self, logger):
        self.visited_shop = False
        self.skipped_cards = False
        self.logger = logger
        # self.logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")

    def combat_choose_next_action(self, playable_cards, monsters, combat):
        playable_card_names = [card.name for card in playable_cards]

        player = combat.player
        enemies = combat.enemies
        enemy_intents = [enemy.intent for enemy in enemies]
        enemy_healths = [enemy.health for enemy in enemies]
        enemy_blocks = [enemy.block for enemy in enemies]
        hand = player.deck.hand
        draw_pile = player.deck.draw_pile
        discard_pile = player.deck.discard_pile
        exhaust_pile = player.deck.exhaust_pile


        card_results = {}
        playable_sim_cards = [card for i, card in enumerate(hand) if card.name in playable_card_names]
        for card in playable_sim_cards:
            player.deck.hand = copy.deepcopy(hand)
            player.deck.draw_pile = copy.deepcopy(draw_pile)
            player.deck.discard_pile = copy.deepcopy(discard_pile)
            player.deck.exhaust_pile = copy.deepcopy(exhaust_pile)

            player.health = player.health
            player.block = player.block
            player.energy = player.energy
            for i, enemy in enumerate(enemies):
                enemy.health = enemy_healths[i]
                enemy.block = enemy_blocks[i]
                enemy.intent = enemy_intents[i]

            target_enemy = random.choice(enemies)
            card_to_play = [player_card for player_card in player.deck.hand if player_card.name == card.name][0]
            self.logger.write("Playing " + card_to_play.name + " on enemy " + str(target_enemy))

            enemy_health, player_health = combat.run_turn(card_to_play, target_enemy)
            self.logger.write("Enemy health at " + str(target_enemy.health) + " after playing " + card.name)
            card_results[card.name] = [enemy_health, player_health]

        self.logger.write("After playing each, card results found: " + str(card_results))

        best = max(card_results, key=lambda x: card_results.get(x)[1])
        best_value = card_results.get(best)[1]
        best_cards = [card for card, values in card_results.items() if values[1] == best_value]
        best_cards = sorted(best_cards, key=lambda x: card_results[x][0], reverse=False)

        self.logger.write("Best card order: " + str(best_cards))

        card_to_play = best_cards[0]
        card_to_play = playable_cards[playable_card_names.index(card_to_play)]

        if len(playable_cards) == 0:
            return EndTurnAction()
        # card_to_play = random.choice(playable_cards)
        # TODO: FINISH!
        if card_to_play.has_target:
            available_monsters = [monster for monster in monsters if
                                  monster.current_hp > 0 and not monster.half_dead and not monster.is_gone]
            if len(available_monsters) == 0:
                return EndTurnAction()
            target = random.choice(available_monsters)
            self.logger.write("Playing " + card_to_play.name + " on " + target.name)
            return PlayCardAction(card=card_to_play, target_monster=target)
        else:
            self.logger.write("Playing " + card_to_play.name)
            return PlayCardAction(card=card_to_play)

    def scry(self, cards, enemies, player_state):
        return [random.choice([True, False]) for _ in cards]

    def choose_option(self, state):
        if state.screen_type == ScreenType.EVENT:
            if state.screen.event_id in ["Vampires", "Masked Bandits", "Knowing Skull", "Ghosts", "Liars Game",
                                              "Golden Idol", "Drug Dealer", "The Library"]:
                return ChooseAction(len(state.screen.options) - 1)
            else:
                return ChooseAction(0)
        if state.screen_type == ScreenType.CHEST:
            self.logger.write("Opening chest...")
            return OpenChestAction()
        if state.screen_type == ScreenType.SHOP_ROOM:
            if not self.visited_shop:
                self.visited_shop = True
                self.logger.write("Entering shop...")
                return ChooseShopkeeperAction()
            else:
                self.logger.write("Leaving shop and Proceeding...")
                self.visited_shop = False
                return ProceedAction()
        elif state.screen_type == ScreenType.REST:
            self.logger.write("Rest options available")
            return self.choose_rest_option(state)
        elif state.screen_type == ScreenType.CARD_REWARD:
            self.logger.write("Card rewardds available")
            return self.choose_card_reward(state)
        elif state.screen_type == ScreenType.COMBAT_REWARD:
            for reward_item in state.screen.rewards:
                if reward_item.reward_type == RewardType.POTION and state.are_potions_full():
                    continue
                elif reward_item.reward_type == RewardType.CARD and self.skipped_cards:
                    continue
                else:
                    return CombatRewardAction(reward_item)
            self.skipped_cards = False
            return ProceedAction()
        elif state.screen_type == ScreenType.MAP:
            return self.make_map_choice(state)
        elif state.screen_type == ScreenType.BOSS_REWARD:
            relics = state.screen.relics
            # best_boss_relic = self.priorities.get_best_boss_relic(relics)
            return BossRewardAction(random.choice(relics))
        elif state.screen_type == ScreenType.SHOP_SCREEN:
            if state.screen.purge_available and state.gold >= state.screen.purge_cost:
                self.logger.write("Choosing purge...")
                return ChooseAction(name="purge")
            for relic in state.screen.relics:
                if state.gold >= relic.price:
                    return BuyRelicAction(relic)
            for card in state.screen.cards:
                if state.gold >= card.price and random.randint(0, 1) == 0:
                    return BuyCardAction(card)
            return CancelAction()
        elif state.screen_type == ScreenType.GRID:
            if not state.choice_available:
                return ProceedAction()
            else:
                num_cards = state.screen.num_cards
                choices = []
                for i in range(num_cards):
                    choices.append(random.choice(state.screen.cards))
                return CardSelectAction(choices)
        elif state.screen_type == ScreenType.HAND_SELECT:
            if not state.choice_available:
                return ProceedAction()
                # Usually, we don't want to choose the whole hand for a hand select. 3 seems like a good compromise.
            num_cards = min(state.screen.num_cards, 3)
            cards = state.screen.cards
            choices = []
            for i in range(num_cards):
                choices.append(random.choice(cards))
                cards.remove(cards[i])
            return CardSelectAction(choices)
        else:
            return ProceedAction()

    def choose_rest_option(self, state):
        options = state.screen.rest_options
        if len(options) > 0 and not state.screen.has_rested:
            choice = random.choice(options)
            self.logger.write("Choosing " + str(choice) + "...")
            return RestAction(random.choice(options))
        else:
            self.logger.write("Proceeding and leaving rest area...")
            return ProceedAction()

    def choose_card_reward(self, state):
        cards = state.screen.cards
        choice = random.choice(cards)
        self.logger.write("Choosing " + choice.name + "...")
        return CardRewardAction(choice)

    def make_map_choice(self, state):
        if state.screen.boss_available:
            return ChooseMapBossAction()
        if len(state.screen.next_nodes) > 0:
            choice = random.choice(state.screen.next_nodes)
            return ChooseMapNodeAction(choice)
        return ChooseMapNodeAction(0)
