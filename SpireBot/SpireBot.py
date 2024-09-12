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

    def create_cards(self, names: list, player: Player):
        cards = []
        for card in names:
            module = importlib.import_module("CombatSim.Actions.Library." + card.replace(' ', ''))
            class_ = getattr(module, card.replace(' ', ''))
            cards.append(class_(player))
        return cards

    def combat_choose_next_action(self, state):
        playable_cards = [card for card in state.hand if card.is_playable]
        playable_card_names = [card.name for card in playable_cards]

        enemies = []
        enemy_intents = []
        for monster in state.monsters:
            monster_name = monster.name.replace(" ", "")
            if "(S)" in monster_name:
                monster_name = monster_name.replace("(S)", "Small")
            if "(M)" in monster_name:
                monster_name = monster_name.replace("(M)", "Medium")
            if "(L)" in monster_name:
                monster_name = monster_name.replace("(L)", "Large")
            if "Louse" in monster_name:
                if monster.monster_id == "FuzzyLouseDefensive":
                    monster_name = "GreenLouse"
                else:
                    monster_name = "RedLouse"
            if "Slaver" in monster_name:
                if monster.monster_id == "SlaverBlue":
                    monster_name = "BlueSlaver"
                else:
                    monster_name = "RedSlaver"
            module = importlib.import_module("CombatSim.Entities.Dungeon." + monster_name)
            class_ = getattr(module, monster_name)
            enemy = class_(state.ascension_level, state.act)
            enemy.health = monster.current_hp
            enemy.block = monster.block

            self.logger.write(monster_name + " intent is " + str(monster.intent))
            possible_intents = [intent for intent in enemy.intent_set if intent.intent_type == monster.intent]
            if len(possible_intents) > 1:
                if monster.intent == char.Intent.ATTACK:
                    enemy.intent = [intent for intent in enemy.intent_set if intent.damage == monster.move_base_damage][0]
                else:
                    enemy.intent = random.choice(enemy.intent)
            else:
                enemy.intent = possible_intents[0]

            enemy_intents.append(enemy.intent)

            self.logger.write("Detected " + monster_name + " intent as " + str(enemy.intent))

            enemies.append(class_(state.ascension_level, state.act))
        player = Player(state.player.current_hp, state.player.energy, state.gold, state.potions, state.relics, [])
        draw_pile = self.create_cards([card.name for card in state.draw_pile], player)
        hand = self.create_cards([card.name for card in state.hand], player)

        self.logger.write("Starting hand is: " + str(hand))

        discard_pile = self.create_cards([card.name for card in state.discard_pile], player)
        exhaust_pile = self.create_cards([card.name for card in state.exhaust_pile], player)
        player.block = state.player.block
        player.energy = state.player.energy
        combat = Combat(player, enemies, debug=False)
        card_results = {}
        playable_sim_cards = [card for i, card in enumerate(hand) if card.name in playable_card_names]
        for card in playable_sim_cards:
            player.deck.hand = copy.deepcopy(hand)
            player.deck.draw_pile = copy.deepcopy(draw_pile)
            player.deck.discard_pile = copy.deepcopy(discard_pile)
            player.deck.exhaust_pile = copy.deepcopy(exhaust_pile)

            player.health = state.player.current_hp
            player.block = state.player.block
            player.energy = state.player.energy
            for i, enemy in enumerate(enemies):
                enemy.health = state.monsters[i].current_hp
                enemy.block = state.monsters[i].block
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
            available_monsters = [monster for monster in state.monsters if
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
