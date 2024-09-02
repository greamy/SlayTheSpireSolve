import json
import random
import time

from spirecomm.communication.action import *
from spirecomm.spire.game import Game


class SpireBot:
    def __init__(self):
        self.state = None
        self.visited_shop = False
        self.skipped_cards = False
        # self.logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")

    def get_next_action(self, game_state: Game):
        self.state = game_state
        if self.state.choice_available:
            return self.choose_option()
        if self.state.proceed_available:
            return ProceedAction()
        if self.state.play_available:
            # TODO: Play potions and cards
            return self.combat_choose_next_action()
        if self.state.end_available:
            return EndTurnAction()
        if self.state.cancel_available:
            return CancelAction()

    def combat_choose_next_action(self):
        playable_cards = [card for card in self.state.hand if card.is_playable]
        if len(playable_cards) == 0:
            return EndTurnAction()
        card_to_play = random.choice(playable_cards)
        # TODO: FINISH!
        return random.choice(playable_cards)

    def scry(self, cards, enemies, player_state):
        return [random.choice([True, False]) for _ in cards]

    def choose_option(self):
        if self.state.screen_type == ScreenType.EVENT:
            if self.state.screen.event_id in ["Vampires", "Masked Bandits", "Knowing Skull", "Ghosts", "Liars Game",
                                              "Golden Idol", "Drug Dealer", "The Library"]:
                return ChooseAction(len(self.state.screen.options) - 1)
            else:
                return ChooseAction(0)
        if self.state.screen_type == ScreenType.CHEST:
            return OpenChestAction()
        if self.state.screen_type == ScreenType.SHOP_ROOM:
            if not self.visited_shop:
                self.visited_shop = True
                return ChooseShopkeeperAction()
            else:
                self.visited_shop = False
                ProceedAction()
        elif self.state.screen_type == ScreenType.REST:
            return self.choose_rest_option()
        elif self.state.screen_type == ScreenType.CARD_REWARD:
            return self.choose_card_reward()
        elif self.state.screen_type == ScreenType.COMBAT_REWARD:
            for reward_item in self.state.screen.rewards:
                if reward_item.reward_type == RewardType.POTION and self.state.are_potions_full():
                    continue
                elif reward_item.reward_type == RewardType.CARD and self.skipped_cards:
                    continue
                else:
                    return CombatRewardAction(reward_item)
            self.skipped_cards = False
            return ProceedAction()
        elif self.state.screen_type == ScreenType.MAP:
            pass
            # return self.make_map_choice()
        elif self.state.screen_type == ScreenType.BOSS_REWARD:
            relics = self.state.screen.relics
            # best_boss_relic = self.priorities.get_best_boss_relic(relics)
            return BossRewardAction(random.choice(relics))
        elif self.state.screen_type == ScreenType.SHOP_SCREEN:
            if self.state.screen.purge_available and self.state.gold >= self.state.screen.purge_cost:
                return ChooseAction(name="purge")
            for relic in self.state.screen.relics:
                if self.state.gold >= relic.price:
                    return BuyRelicAction(relic)
            for card in self.state.screen.cards:
                if self.state.gold >= card.price and random.randint(0, 1) == 0:
                    return BuyCardAction(card)
            return CancelAction()
        elif self.state.screen_type == ScreenType.GRID:
            if not self.state.choice_available:
                return ProceedAction()
            else:
                num_cards = self.state.screen.num_cards
                choices = []
                for i in range(num_cards):
                    choices.append(random.choice(self.state.screen.cards))
                return CardSelectAction(choices)
        elif self.state.screen_type == ScreenType.HAND_SELECT:
            if not self.state.choice_available:
                return ProceedAction()
                # Usually, we don't want to choose the whole hand for a hand select. 3 seems like a good compromise.
            num_cards = min(self.state.screen.num_cards, 3)
            cards = self.state.screen.cards
            choices = []
            for i in range(num_cards):
                choices.append(random.choice(cards))
                cards.remove(cards[i])
            return CardSelectAction(choices)
        else:
            return ProceedAction()

    def choose_rest_option(self):
        options = self.state.screen.rest_options
        if len(options) > 0 and not self.state.screen.has_rested:
            return RestAction(random.choice(options))
        else:
            return ProceedAction()

    def choose_card_reward(self):
        cards = self.state.screen.cards
        choice = random.choice(cards)
        return CardRewardAction(choice)
