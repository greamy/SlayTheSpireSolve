import random

import pygame

from CombatSim.Entities.Player import Player
from GameSim.Map.Room import Room
from GameSim.Render.Renderer import Renderer


# Watcher card pools by rarity (no colorless cards, no starter Strike/Defend)
_COMMON_ATTACKS = {"Eruption", "FlurryofBlows", "CrushJoints", "BowlingBash", "FollowUp", "SashWhip"}
_COMMON_SKILLS = {"Prostrate", "Protect", "Tranquility", "Evaluate", "Pray", "EmptyFist"}
_COMMON_POWERS = {"Study", "Devotion"}

_UNCOMMON_ATTACKS = {"Tantrum", "Expunger", "CarveReality", "Weave", "Smite", "Wallop", "WindmillStrike"}
_UNCOMMON_SKILLS = {
    "WaveoftheHand", "Conclude", "EmptyBody", "EmptyMind", "Vigilance", "ThirdEye",
    "InnerPeace", "Indignation", "MentalFortress", "TalktotheHand", "FearNoEvil", "Sanctity",
}
_UNCOMMON_POWERS = {"Nirvana", "Foresight", "Swivel", "BattleHymn", "PressurePoints", "Rushdown", "Fasting", "LikeWater"}

_RARE_ATTACKS = {"WheelKick", "Brilliance", "LessonLearned", "Ragnarok", "ThroughViolence", "Alpha"}
_RARE_SKILLS = {"SpiritShield", "Vault", "Meditate", "WreathofFlame"}
_RARE_POWERS = {"DevaForm", "MasterReality", "Collect", "Omniscience", "ConjureBlade"}

_PRICE_RANGES = {
    'common':   (45, 55),
    'uncommon': (68, 83),
    'rare':     (135, 165),
}
_RELIC_PRICE_RANGE = (143, 315)


class ShopRoom(Room):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "S", floor, x, prev_rooms, next_rooms, act, ascension)

        # Shop inventory — generated in start()
        self.card_names: list[str] = []
        self.card_prices: list[int] = []
        self.card_bought: list[bool] = []

        self.shop_relics: list = []        # Relic instances
        self.relic_prices: list[int] = []
        self.relic_bought: list[bool] = []

        self.remove_card_available = True

        # render attributes
        self.color = (255, 215, 0)  # Gold

        self.btn_width = 200
        self.btn_height = 40
        self.item_start_y = 80
        self.item_spacing = 50
        self.relic_start_y = 380

    def start(self):
        self._generate_shop()

    def _get_rarity(self, name: str) -> str:
        if name in _COMMON_ATTACKS or name in _COMMON_SKILLS or name in _COMMON_POWERS:
            return 'common'
        if name in _UNCOMMON_ATTACKS or name in _UNCOMMON_SKILLS or name in _UNCOMMON_POWERS:
            return 'uncommon'
        return 'rare'

    def _generate_shop(self):
        implemented = self.player.implemented_cards

        def available(pool):
            return [name for name in pool if name in implemented]

        attack_pool = available(_COMMON_ATTACKS) + available(_UNCOMMON_ATTACKS) + available(_RARE_ATTACKS)
        skill_pool  = available(_COMMON_SKILLS)  + available(_UNCOMMON_SKILLS)  + available(_RARE_SKILLS)
        power_pool  = available(_COMMON_POWERS)  + available(_UNCOMMON_POWERS)  + available(_RARE_POWERS)

        picks = []
        for pool, count in ((attack_pool, 2), (skill_pool, 2), (power_pool, 1)):
            pool = list(pool)
            random.shuffle(pool)
            for name in pool[:count]:
                rarity = self._get_rarity(name)
                lo, hi = _PRICE_RANGES[rarity]
                picks.append((name, random.randint(lo, hi)))

        self.card_names  = [p[0] for p in picks]
        self.card_prices = [p[1] for p in picks]
        self.card_bought = [False] * len(picks)

        relic_names = list(self.player.implemented_relics.keys())
        chosen_relic_names = random.sample(relic_names, min(3, len(relic_names))) if relic_names else []
        self.shop_relics   = []
        self.relic_prices  = []
        self.relic_bought  = []
        for rname in chosen_relic_names:
            cls = getattr(self.player.implemented_relics[rname], rname)
            self.shop_relics.append(cls(self.player))
            self.relic_prices.append(random.randint(*_RELIC_PRICE_RANGE))
            self.relic_bought.append(False)

        # One random item gets a 50% discount
        total = len(self.card_names) + len(self.shop_relics)
        if total > 0:
            idx = random.randrange(total)
            if idx < len(self.card_names):
                self.card_prices[idx] = max(1, self.card_prices[idx] // 2)
            else:
                ridx = idx - len(self.card_names)
                self.relic_prices[ridx] = max(1, self.relic_prices[ridx] // 2)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font, render_type):
        if not self.card_names and not self.shop_relics:
            self._generate_shop()

        if render_type == Renderer.RenderType.PYGAME:
            # --- PYGAME rendering ---
            pygame.draw.rect(screen, (30, 20, 10), (0, 0, screen_size[0], screen_size[1]))

            title = font.render("Merchant", True, (255, 215, 0))
            screen.blit(title, (screen_size[0] // 2 - title.get_width() // 2, 20))

            # Cards for sale
            cards_label = font.render("Cards:", True, (200, 200, 200))
            screen.blit(cards_label, (30, 60))

            for i, (name, price, bought) in enumerate(zip(self.card_names, self.card_prices, self.card_bought)):
                y = self.item_start_y + i * self.item_spacing
                color = (80, 80, 80) if bought else (50, 100, 180)
                pygame.draw.rect(screen, color, (30, y, self.btn_width, self.btn_height))
                label = font.render(f"{name}  {price}g", True, (255, 255, 255) if not bought else (150, 150, 150))
                screen.blit(label, (40, y + 10))

            # Relics for sale
            relics_label = font.render("Relics:", True, (200, 200, 200))
            screen.blit(relics_label, (30, self.relic_start_y - 30))

            for i, (relic, price, bought) in enumerate(zip(self.shop_relics, self.relic_prices, self.relic_bought)):
                y = self.relic_start_y + i * self.item_spacing
                color = (80, 80, 80) if bought else (150, 80, 20)
                pygame.draw.rect(screen, color, (30, y, self.btn_width, self.btn_height))
                label = font.render(f"{relic.name}  {price}g", True, (255, 255, 255) if not bought else (150, 150, 150))
                screen.blit(label, (40, y + 10))

            # Card removal service
            remove_y = screen_size[1] - 120
            remove_cost = self.player.shop_remove_cost
            if self.remove_card_available:
                pygame.draw.rect(screen, (120, 30, 30), (30, remove_y, self.btn_width + 50, self.btn_height))
                remove_label = font.render(f"Remove Card  {remove_cost}g", True, (255, 255, 255))
            else:
                pygame.draw.rect(screen, (60, 30, 30), (30, remove_y, self.btn_width + 50, self.btn_height))
                remove_label = font.render("Remove Card  (used)", True, (150, 150, 150))
            screen.blit(remove_label, (40, remove_y + 10))

            # Exit button
            exit_y = screen_size[1] - 60
            pygame.draw.rect(screen, (60, 60, 60), (30, exit_y, 120, self.btn_height))
            exit_label = font.render("Leave", True, (255, 255, 255))
            screen.blit(exit_label, (40, exit_y + 10))

        if (self.remove_card_available
                and self.player.deck.draw_pile
                and self.player.gold >= self.player.shop_remove_cost):
            chosen = self.player.controller.select_cards_from_zone(
                self.player, Player.Deck.Zone.DRAW_PILE, [], 1, False,
                prefer_outlier=True,
            )
            if chosen:
                card = self.player.deck.draw_pile[chosen[0]]
                self.player.gold -= self.player.shop_remove_cost
                self.player.shop_remove_cost += 25
                self.player.deck.remove_card(card)
                self.remove_card_available = False

        if not self.player.controller.wait_for_counter():
            return True

        return False

    def handle_event(self, event):
        if event.button != 1:
            return
        pos = pygame.mouse.get_pos()
        screen_h = pygame.display.get_surface().get_height()

        # Card purchases
        for i in range(len(self.card_names)):
            y = self.item_start_y + i * self.item_spacing
            if (30 < pos[0] < 30 + self.btn_width and y < pos[1] < y + self.btn_height
                    and not self.card_bought[i]
                    and self.player.gold >= self.card_prices[i]):
                self.player.gold -= self.card_prices[i]
                self.player.add_card(self.card_names[i])
                self.card_bought[i] = True

        # Relic purchases
        for i in range(len(self.shop_relics)):
            y = self.relic_start_y + i * self.item_spacing
            if (30 < pos[0] < 30 + self.btn_width and y < pos[1] < y + self.btn_height
                    and not self.relic_bought[i]
                    and self.player.gold >= self.relic_prices[i]):
                self.player.gold -= self.relic_prices[i]
                self.player.add_relic(self.shop_relics[i])
                self.relic_bought[i] = True

        # Card removal
        remove_y = screen_h - 120
        if (30 < pos[0] < 30 + self.btn_width + 50 and remove_y < pos[1] < remove_y + self.btn_height
                and self.remove_card_available
                and self.player.deck.draw_pile
                and self.player.gold >= self.player.shop_remove_cost):
            chosen = self.player.controller.select_cards_from_zone(
                self.player, Player.Deck.Zone.DRAW_PILE, [], 1, True,
                prefer_outlier=True,
            )
            if chosen:
                card = self.player.deck.draw_pile[chosen[0]]
                self.player.gold -= self.player.shop_remove_cost
                self.player.shop_remove_cost += 25
                self.player.deck.remove_card(card)
                self.remove_card_available = False