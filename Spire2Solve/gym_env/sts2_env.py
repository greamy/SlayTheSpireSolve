"""
STS2 Gymnasium Environment

Wraps the STS2MCP HTTP API (localhost:15526) as a standard gymnasium.Env.
The agent controls combat decisions; non-combat screens (map, rewards, shop,
events, rest sites) are handled automatically by a heuristic fallback policy.

Three classes:
  STS2Client    — thin sync HTTP wrapper around the STS2 REST API
  STS2Vectorizer — translates live JSON state to numpy observation arrays
  STS2Env       — gymnasium.Env implementation
"""

from __future__ import annotations

import time
import random
from typing import Any

import numpy as np
import requests
import gymnasium as gym
from gymnasium import spaces

# ---------------------------------------------------------------------------
# Constants (mirror RLPlayerController.py)
# ---------------------------------------------------------------------------

MAX_HAND_CARDS = 10
MAX_ENEMIES    = 5
CARD_VEC_LEN   = 19
PLAYER_VEC_LEN = 11
ENEMY_VEC_LEN  = 12
STRAT_VEC_LEN  = 10
NUM_ACTIONS    = MAX_HAND_CARDS * MAX_ENEMIES + 1  # 51; last index = end_turn

COMBAT_STATE_TYPES = {"monster", "elite", "boss"}

CARD_TYPE_MAP = {"Attack": 0, "Skill": 1, "Power": 2, "Status": 3, "Curse": 4}
INTENT_TYPE_MAP = {
    "Attack": 0, "Defend": 1, "Buff": 2, "Debuff": 3,
    "Sleep": 4, "Unknown": 5,
}


# ---------------------------------------------------------------------------
# STS2Client
# ---------------------------------------------------------------------------

class STS2Client:
    """Synchronous HTTP client for the STS2MCP singleplayer API."""

    _MAX_RETRIES   = 10
    _RETRY_SLEEP   = 0.05

    def __init__(self, host: str = "localhost", port: int = 15526,
                 timeout: float = 10.0) -> None:
        self._session = requests.Session()
        self._base    = f"http://{host}:{port}/api/v1/singleplayer"
        self._timeout = timeout

    def get_state(self) -> dict:
        """GET current game state, retrying on 'unknown' transitional states."""
        for attempt in range(self._MAX_RETRIES):
            r = self._session.get(self._base, timeout=self._timeout)
            r.raise_for_status()
            state = r.json()
            if state.get("state_type") != "unknown":
                return state
            time.sleep(self._RETRY_SLEEP)
        return state  # return last seen state after exhausting retries

    def post_action(self, body: dict) -> dict:
        """POST a game action. Returns the acknowledgement JSON."""
        r = self._session.post(self._base, json=body, timeout=self._timeout)
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# STS2Vectorizer
# ---------------------------------------------------------------------------

class STS2Vectorizer:
    """
    Converts live STS2 API JSON state to numpy arrays matching the
    shape expected by RLPlayerController / LSTMPPOAgent.

    NOTE: The API does not expose per-card damage/block/attacks values.
    Those 6 features in the 19-dim card vector are zeroed (see TODOs).
    """

    # Status IDs that directly map to simulation modifier fields
    _STRENGTH_ID    = "STRENGTH"
    _VULNERABLE_ID  = "VULNERABLE"
    _WEAK_ID        = "WEAK"

    def parse_cost(self, cost_str: str | None) -> int:
        """Parse energy cost string: "X" or None → 0, otherwise int."""
        if cost_str is None or cost_str == "X":
            return 0
        try:
            return int(cost_str)
        except (ValueError, TypeError):
            return 0

    def _parse_intent_damage(self, label: str | None) -> int:
        try:
            return int(label)
        except (ValueError, TypeError):
            return 0

    def _calc_incoming(self, enemies: list[dict]) -> float:
        total = 0.0
        for enemy in enemies:
            intents = enemy.get("intents") or [{}]
            intent  = intents[0] if intents else {}
            if intent.get("type") == "Attack":
                total += self._parse_intent_damage(intent.get("label"))
        return total

    def get_card_vector(self, card: dict | None, player: dict,
                        enemies: list[dict]) -> np.ndarray:
        """
        19-dim array matching RLPlayerController.get_card_vector.

        Dimensions (0-18):
          0  energy
          1  attacks       [TODO: not in API, zeroed]
          2  stance_calm   [Watcher only, zeroed]
          3  stance_wrath  [Watcher only, zeroed]
          4  stance_divinity [Watcher only, zeroed]
          5  upgraded
          6  draw          [TODO: not in API, zeroed]
          7  exhaust       [TODO: not in API, zeroed]
          8  innate        [TODO: not in API, zeroed]
          9  can_play
          10 card_lethal   [TODO: needs damage, zeroed]
          11 blocks_fully  [TODO: needs block, zeroed]
          12 damage_efficiency [TODO: zeroed]
          13 block_efficiency  [TODO: zeroed]
          14 overkill_amt      [TODO: zeroed]
          15 block_surplus_deficit [TODO: zeroed]
          16 is_attack (one-hot)
          17 is_skill  (one-hot)
          18 is_power  (one-hot)
        """
        if card is None:
            return np.zeros(CARD_VEC_LEN, dtype=np.float32)

        energy    = float(self.parse_cost(card.get("cost")))
        can_play  = float(card.get("can_play", False))
        upgraded  = float(card.get("is_upgraded", False))
        card_type = CARD_TYPE_MAP.get(card.get("type", ""), 0)

        manual = np.array([
            energy,
            0.0,   # attacks — TODO
            0.0,   # stance_calm
            0.0,   # stance_wrath
            0.0,   # stance_divinity
            upgraded,
            0.0,   # draw — TODO
            0.0,   # exhaust — TODO
            0.0,   # innate — TODO
            can_play,
        ], dtype=np.float32)

        features = np.array([
            0.0,   # card_lethal — TODO (no damage info)
            0.0,   # blocks_fully — TODO (no block info)
            0.0,   # damage_efficiency — TODO
            0.0,   # block_efficiency — TODO
            0.0,   # overkill_amt — TODO
            0.0,   # block_surplus_deficit — TODO
            float(card_type == 0),  # is_attack
            float(card_type == 1),  # is_skill
            float(card_type == 2),  # is_power
        ], dtype=np.float32)

        return np.concatenate([manual, features])

    def get_player_vector(self, player: dict) -> np.ndarray:
        """11-dim array matching RLPlayerController.get_player_vector."""
        status_map = {s["id"]: s.get("amount", 0)
                      for s in player.get("status", [])}

        strength    = float(status_map.get(self._STRENGTH_ID, 0))
        is_vuln     = self._VULNERABLE_ID in status_map
        is_weak     = self._WEAK_ID in status_map

        dmg_mult    = 0.75 if is_weak else 1.0
        taken_mult  = 1.5  if is_vuln else 1.0

        return np.array([
            float(player.get("energy", 0)),
            float(player.get("block", 0)),
            0.0,          # block_modifier — not directly in API
            1.0,          # block_multiplier
            strength,     # damage_dealt_modifier (Strength)
            dmg_mult,     # damage_dealt_multiplier (Weak)
            taken_mult,   # damage_taken_multiplier (Vulnerable)
            0.0,          # stance_calm  (Watcher only)
            0.0,          # stance_wrath (Watcher only)
            0.0,          # stance_divinity (Watcher only)
            0.0,          # mantra (Watcher only)
        ], dtype=np.float32)

    def get_enemy_vector(self, enemy: dict) -> np.ndarray:
        """12-dim array matching RLPlayerController.get_enemy_vector."""
        hp     = float(enemy.get("hp",     1))
        max_hp = float(enemy.get("max_hp", 1))
        block  = float(enemy.get("block",  0))
        status_map = {s["id"]: s.get("amount", 0)
                      for s in enemy.get("status", [])}

        intents     = enemy.get("intents") or [{}]
        intent      = intents[0] if intents else {}
        intent_type = intent.get("type", "Unknown")
        intent_int  = INTENT_TYPE_MAP.get(intent_type, 5)
        intent_dmg  = float(self._parse_intent_damage(intent.get("label")))
        intent_atks = 1.0 if intent_type == "Attack" else 0.0
        intent_blk  = intent_dmg if intent_type == "Defend" else 0.0

        return np.array([
            max_hp / hp if hp > 0 else 0.0,  # start_health / health ratio
            block,
            0.0,           # block_modifier
            1.0,           # block_multiplier
            0.0,           # damage_dealt_modifier
            1.0,           # damage_dealt_multiplier
            1.0,           # damage_taken_multiplier
            0.0,           # minion flag (not in API)
            float(intent_int),
            intent_dmg,
            intent_atks,
            intent_blk,
        ], dtype=np.float32)

    def get_strategic_features(self, player: dict, enemies: list[dict],
                                hand: list[dict]) -> np.ndarray:
        """10-dim array matching RLPlayerController.get_strategic_features."""
        raw_incoming = self._calc_incoming(enemies)
        playable     = [c for c in hand if c.get("can_play", False)]

        # damage/block per card not available from API — zeroed
        raw_damage = 0.0  # TODO
        raw_block  = 0.0  # TODO

        hp     = float(player.get("hp",     1))
        max_hp = float(player.get("max_hp", 1))
        blk    = float(player.get("block",  0))

        has_block  = float(any(c.get("type") == "Skill"  for c in playable))
        has_damage = float(any(c.get("type") == "Attack" for c in playable))

        return np.array([
            raw_incoming,
            raw_damage,
            raw_block,
            hp / max_hp if max_hp > 0 else 0.0,
            blk / raw_incoming if raw_incoming > 0 else 1.0,
            0.0,           # has_wrath  (Watcher only)
            0.0,           # has_calm   (Watcher only)
            has_block,
            has_damage,
            float(len(playable)),
        ], dtype=np.float32)

    def get_action_mask(self, hand: list[dict],
                        enemies: list[dict]) -> np.ndarray:
        """
        51-dim float array: 1.0 where action is legal, 0.0 otherwise.

        Layout: action = card_slot * MAX_ENEMIES + target_slot; 50 = end_turn.
        Non-targeted cards (Skill/Power/AllEnemies) are encoded at target_slot=0.
        """
        mask       = np.zeros(NUM_ACTIONS, dtype=np.float32)
        num_en     = len(enemies)
        targeted   = {"AnyEnemy"}

        for i in range(MAX_HAND_CARDS):
            if i >= len(hand):
                break
            card = hand[i]
            if not card.get("can_play", False):
                continue
            if card.get("target_type") in targeted:
                for j in range(num_en):
                    mask[i * MAX_ENEMIES + j] = 1.0
            else:
                mask[i * MAX_ENEMIES + 0] = 1.0

        mask[NUM_ACTIONS - 1] = 1.0  # end_turn always legal
        return mask

    def build_obs(self, state: dict) -> dict[str, np.ndarray]:
        """Convert live API state dict to the gymnasium observation dict."""
        player  = state.get("player", {})
        battle  = state.get("battle", {})
        enemies = battle.get("enemies", [])
        hand    = player.get("hand", [])

        hand_vecs = []
        for i in range(MAX_HAND_CARDS):
            card = hand[i] if i < len(hand) else None
            hand_vecs.append(self.get_card_vector(card, player, enemies))
        hand_arr = np.stack(hand_vecs, axis=0)  # (10, 19)

        enemy_vecs = []
        for i in range(MAX_ENEMIES):
            if i < len(enemies):
                enemy_vecs.append(self.get_enemy_vector(enemies[i]))
            else:
                enemy_vecs.append(np.zeros(ENEMY_VEC_LEN, dtype=np.float32))
        enemies_arr = np.stack(enemy_vecs, axis=0)  # (5, 12)

        enemy_mask = np.array(
            [float(i >= len(enemies)) for i in range(MAX_ENEMIES)],
            dtype=np.float32,
        )

        return {
            "hand":        hand_arr,
            "enemies":     enemies_arr,
            "player":      self.get_player_vector(player),
            "strategic":   self.get_strategic_features(player, enemies, hand),
            "action_mask": self.get_action_mask(hand, enemies),
            "enemy_mask":  enemy_mask,
        }

    def build_deck_array(self, state: dict) -> np.ndarray:
        """
        Variable-length (N, CARD_VEC_LEN) array from current hand cards.

        NOTE: draw/discard/exhaust pile cards in the API are simplified objects
        (name/cost/description only) and cannot be fully vectorized. This array
        reflects hand cards only. Pass in info["deck"] to the training loop.
        """
        player  = state.get("player", {})
        battle  = state.get("battle", {})
        enemies = battle.get("enemies", [])
        hand    = player.get("hand", [])
        if not hand:
            return np.zeros((0, CARD_VEC_LEN), dtype=np.float32)
        vecs = [self.get_card_vector(c, player, enemies) for c in hand]
        return np.stack(vecs, axis=0)


# ---------------------------------------------------------------------------
# STS2Env
# ---------------------------------------------------------------------------

class STS2Env(gym.Env):
    """
    Gymnasium environment for Slay the Spire 2 via the STS2MCP HTTP API.

    Observation space: Dict with combat vectors (hand, enemies, player,
                       strategic, action_mask, enemy_mask).
    Action space:      Discrete(51) — (card_slot * 5 + target_slot) or 50=end_turn.
    info["deck"]:      Variable-length (N, 19) deck array (hand cards only).

    Prerequisites:
    - STS2 running with STS2MCP mod loaded (HTTP server on localhost:15526).
    - Game at the main menu before calling reset().

    Usage:
        env = STS2Env(character_id="IRONCLAD")
        obs, info = env.reset()
        action, log_prob, value, _ = agent.choose_action(
            agent._convert_state_to_tensors({**obs, "deck": info["deck"]})
        )
        obs, reward, terminated, truncated, info = env.step(action)
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        character_id: str = "IRONCLAD",
        max_steps:    int = 1000,
        host:         str = "localhost",
        port:         int = 15526,
    ) -> None:
        super().__init__()
        self._client      = STS2Client(host=host, port=port)
        self._vectorizer  = STS2Vectorizer()
        self._character   = character_id.upper()
        self._max_steps   = max_steps

        self.observation_space = spaces.Dict({
            "hand":        spaces.Box(-np.inf, np.inf,
                               shape=(MAX_HAND_CARDS, CARD_VEC_LEN), dtype=np.float32),
            "enemies":     spaces.Box(-np.inf, np.inf,
                               shape=(MAX_ENEMIES, ENEMY_VEC_LEN),   dtype=np.float32),
            "player":      spaces.Box(-np.inf, np.inf,
                               shape=(PLAYER_VEC_LEN,),               dtype=np.float32),
            "strategic":   spaces.Box(-np.inf, np.inf,
                               shape=(STRAT_VEC_LEN,),                dtype=np.float32),
            "action_mask": spaces.Box(0.0, 1.0,
                               shape=(NUM_ACTIONS,),                  dtype=np.float32),
            "enemy_mask":  spaces.Box(0.0, 1.0,
                               shape=(MAX_ENEMIES,),                  dtype=np.float32),
        })
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        # Runtime state
        self._last_state:          dict      = {}
        self._turn_start_hand:     list[dict] = []
        self._turn_start_enemies:  list[dict] = []
        self._played_slots:        set[int]   = set()
        self._step_count:          int        = 0
        self._prev_player_hp:      int        = 0
        self._prev_enemy_total_hp: int        = 0

    # ------------------------------------------------------------------
    # Public gym interface
    # ------------------------------------------------------------------

    def reset(self, seed=None, options=None
              ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        super().reset(seed=seed)
        self._step_count = 0

        self._navigate_to_first_combat()
        state = self._last_state

        self._prev_player_hp      = state["player"]["hp"]
        self._prev_enemy_total_hp = self._sum_enemy_hp(state)
        self._start_turn(state)

        obs  = self._vectorizer.build_obs(state)
        info = {
            "state_type": state["state_type"],
            "deck":       self._vectorizer.build_deck_array(state),
        }
        return obs, info

    def step(self, action: int
             ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        self._step_count += 1

        # 1. Send action
        error = self._send_action(action)
        if error is not None:
            obs = self._vectorizer.build_obs(self._last_state)
            return obs, -0.05, False, False, {"error": error,
                                               "deck": self._vectorizer.build_deck_array(self._last_state)}

        # 2. Poll until player's turn or episode ends
        state = self._poll_until_player_turn_or_end()
        st    = state.get("state_type")

        # 3. Handle non-combat screens automatically
        if st not in COMBAT_STATE_TYPES and st != "game_over":
            state = self._advance_through_noncombat(state)
            st    = state.get("state_type")

        self._last_state = state

        # 4. Compute reward
        reward = self._compute_reward(state, st)

        # 5. Termination
        terminated = st == "game_over" or state.get("player", {}).get("hp", 1) <= 0
        truncated  = self._step_count >= self._max_steps

        # 6. If new combat, snapshot the turn
        if not terminated and st in COMBAT_STATE_TYPES:
            if state.get("battle", {}).get("turn") == "player":
                self._start_turn(state)

        obs  = self._vectorizer.build_obs(state)
        info = {
            "state_type": st,
            "deck":       self._vectorizer.build_deck_array(state),
        }
        return obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # Action dispatch
    # ------------------------------------------------------------------

    def _send_action(self, action: int) -> str | None:
        """Translate flat action int to API call. Returns error string or None."""
        if action == NUM_ACTIONS - 1:
            result = self._client.post_action({"action": "end_turn"})
            self._played_slots = set()
        else:
            stable_slot = action // MAX_ENEMIES
            target_slot = action % MAX_ENEMIES
            result = self._play_card(stable_slot, target_slot)

        if result.get("status") == "error":
            return result.get("error", "unknown error")
        return None

    def _play_card(self, stable_slot: int, target_slot: int) -> dict:
        """
        Map a stable-hand-slot action to the correct live card_index,
        accounting for index shift when earlier cards have been played.
        """
        if stable_slot >= len(self._turn_start_hand):
            return {"status": "error", "error": f"stable_slot {stable_slot} out of range"}

        played_below  = sum(1 for ps in self._played_slots if ps < stable_slot)
        current_index = stable_slot - played_below

        body: dict[str, Any] = {"action": "play_card", "card_index": current_index}

        card        = self._turn_start_hand[stable_slot]
        target_type = card.get("target_type", "")
        if target_type == "AnyEnemy":
            if target_slot < len(self._turn_start_enemies):
                body["target"] = self._turn_start_enemies[target_slot]["entity_id"]
            else:
                return {"status": "error", "error": f"target_slot {target_slot} out of range"}

        result = self._client.post_action(body)
        if result.get("status") != "error":
            self._played_slots.add(stable_slot)
        return result

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def _navigate_to_first_combat(self, max_iters: int = 300) -> None:
        """Drive the game from any state to the first player turn of a combat."""
        for _ in range(max_iters):
            state = self._client.get_state()
            st    = state.get("state_type")

            if st in COMBAT_STATE_TYPES:
                if state.get("battle", {}).get("turn") == "player":
                    self._last_state = state
                    return
                # Enemy turn or transitional state — keep polling
                time.sleep(0.1)
                continue

            if st == "menu":
                self._handle_menu(state)
            elif st == "game_over":
                self._client.post_action({"action": "menu_select", "option": "main_menu"})
            else:
                self._handle_noncombat(state)

            time.sleep(0.1)

        raise RuntimeError("STS2Env: could not reach first combat within timeout. "
                           "Ensure the game is at the main menu and the mod is loaded.")

    def _handle_menu(self, state: dict) -> None:
        screen  = state.get("menu_screen", "main")
        options = state.get("options", [])
        # Normalise options list (may be list of strings or dicts)
        opt_names = [
            (o["name"] if isinstance(o, dict) else o).lower()
            for o in options
        ]

        if screen == "main":
            if "singleplayer" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "singleplayer"})
        elif screen == "singleplayer":
            if "standard" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "standard"})
        elif screen == "character_select":
            char_lower = self._character.lower()
            # Select the character if it's in the options list
            if char_lower in opt_names:
                self._client.post_action({"action": "menu_select", "option": self._character})
                time.sleep(0.3)
            # Always follow up with confirm/embark in the same iteration so we
            # don't loop forever re-selecting the character without starting the run.
            if "confirm" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "confirm"})
            elif "embark" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "embark"})
        elif screen == "tutorial_prompt":
            self._client.post_action({"action": "menu_select", "option": "no"})
        elif screen == "profile_select":
            self._client.post_action({"action": "menu_select", "option": "profile_1"})
        elif screen == "popup":
            if "ignore" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "ignore"})
            elif "back" in opt_names:
                self._client.post_action({"action": "menu_select", "option": "back"})

    def _advance_through_noncombat(self, state: dict,
                                    max_iters: int = 200) -> dict:
        """
        Repeatedly apply heuristic non-combat actions until reaching a combat
        or game_over state.
        """
        for _ in range(max_iters):
            st = state.get("state_type")
            if st in COMBAT_STATE_TYPES or st == "game_over":
                return state
            self._handle_noncombat(state)
            time.sleep(0.1)
            state = self._client.get_state()
        return state

    def _handle_noncombat(self, state: dict) -> None:
        """Single heuristic step for a non-combat screen."""
        st = state.get("state_type")

        if st == "rewards":
            self._auto_claim_rewards(state)

        elif st == "card_reward":
            if state["card_reward"].get("can_skip"):
                self._client.post_action({"action": "skip_card_reward"})
            else:
                cards = state["card_reward"].get("cards", [])
                if cards:
                    idx = random.randint(0, len(cards) - 1)
                    self._client.post_action({"action": "select_card_reward",
                                              "card_index": idx})

        elif st == "map":
            options = state["map"].get("next_options", [])
            if options:
                self._client.post_action({"action": "choose_map_node",
                                          "index": options[0]["index"]})

        elif st == "event":
            ev = state.get("event", {})
            if ev.get("in_dialogue"):
                self._client.post_action({"action": "advance_dialogue"})
            else:
                opts = [o for o in ev.get("options", [])
                        if not o.get("is_locked", True)]
                if opts:
                    self._client.post_action({"action": "choose_event_option",
                                              "index": opts[0]["index"]})

        elif st == "rest_site":
            rs   = state.get("rest_site", {})
            opts = [o for o in rs.get("options", []) if o.get("is_enabled", False)]
            if opts:
                self._client.post_action({"action": "choose_rest_option",
                                          "index": opts[0]["index"]})
            elif rs.get("can_proceed"):
                self._client.post_action({"action": "proceed"})

        elif st in ("shop", "treasure", "fake_merchant"):
            self._client.post_action({"action": "proceed"})

        elif st == "relic_select":
            relics = state.get("relic_select", {}).get("relics", [])
            if relics:
                self._client.post_action({"action": "select_relic",
                                          "index": relics[0]["index"]})

        elif st == "card_select":
            cs = state.get("card_select", {})
            if cs.get("can_cancel"):
                self._client.post_action({"action": "cancel_selection"})

        elif st == "bundle_select":
            bs = state.get("bundle_select", {})
            if bs.get("can_cancel"):
                self._client.post_action({"action": "cancel_bundle_selection"})

        elif st == "hand_select":
            hs    = state.get("hand_select", {})
            cards = hs.get("cards", [])
            if cards:
                self._client.post_action({"action": "combat_select_card",
                                          "card_index": cards[0]["index"]})
                if hs.get("can_confirm"):
                    self._client.post_action({"action": "combat_confirm_selection"})

        elif st == "crystal_sphere":
            cs = state.get("crystal_sphere", {})
            if cs.get("can_proceed"):
                self._client.post_action({"action": "crystal_sphere_proceed"})
            else:
                cells = cs.get("clickable_cells", [])
                if cells:
                    c = cells[0]
                    self._client.post_action({"action": "crystal_sphere_click_cell",
                                              "x": c["x"], "y": c["y"]})

        elif st == "menu":
            self._handle_menu(state)

        # unknown / overlay: do nothing this iteration; caller will retry

    def _auto_claim_rewards(self, state: dict) -> None:
        """Claim all non-card rewards, then proceed (skipping card reward)."""
        items = state.get("rewards", {}).get("items", [])
        # Claim from highest index first so indices don't shift mid-loop
        for item in sorted(items, key=lambda x: x["index"], reverse=True):
            if item["type"] != "card":
                self._client.post_action({"action": "claim_reward",
                                          "index": item["index"]})
                time.sleep(0.05)
        if state["rewards"].get("can_proceed"):
            self._client.post_action({"action": "proceed"})

    # ------------------------------------------------------------------
    # Polling
    # ------------------------------------------------------------------

    def _poll_until_player_turn_or_end(
        self,
        max_polls:     int   = 100,
        poll_interval: float = 0.1,
        initial_sleep: float = 0.2,
    ) -> dict:
        """
        After submitting an action, wait until:
          - It's the player's turn again (combat continues), OR
          - A non-combat screen appeared (combat ended), OR
          - game_over.

        initial_sleep: brief delay before first poll to avoid reading
        stale player-turn state immediately after end_turn POST.
        """
        time.sleep(initial_sleep)
        for _ in range(max_polls):
            state = self._client.get_state()
            st    = state.get("state_type")

            if st == "game_over":
                return state
            if st not in COMBAT_STATE_TYPES:
                return state  # rewards / map / etc.
            battle = state.get("battle", {})
            if battle.get("turn") == "player" and battle.get("is_play_phase", True):
                return state

            time.sleep(poll_interval)

        return state  # return whatever we have after timeout

    # ------------------------------------------------------------------
    # Reward and bookkeeping
    # ------------------------------------------------------------------

    def _compute_reward(self, state: dict, state_type: str) -> float:
        """
        Mirrors RLPlayerController reward shaping:
          per-turn:  hp_delta * -0.04 + enemy_hp_delta * 0.04
          combat-win: +0.1 + hp_ratio * 0.2  (reached non-combat alive)
        """
        player = state.get("player", {})
        curr_player_hp   = player.get("hp", 0)
        curr_enemy_total = self._sum_enemy_hp(state)

        hp_lost     = self._prev_player_hp      - curr_player_hp
        damage_done = self._prev_enemy_total_hp  - curr_enemy_total

        reward  = hp_lost     * -0.04
        reward += damage_done *  0.04

        if state_type not in COMBAT_STATE_TYPES and state_type != "game_over":
            if curr_player_hp > 0:
                max_hp       = player.get("max_hp", max(curr_player_hp, 1))
                health_ratio = curr_player_hp / max_hp
                reward += 0.1 + health_ratio * 0.2

        self._prev_player_hp      = curr_player_hp
        self._prev_enemy_total_hp = curr_enemy_total
        return reward

    def _start_turn(self, state: dict) -> None:
        """Snapshot hand and enemy list at the start of a player turn."""
        player = state.get("player", {})
        battle = state.get("battle", {})
        self._turn_start_hand    = list(player.get("hand", []))
        self._turn_start_enemies = list(battle.get("enemies", []))
        self._played_slots       = set()
        self._prev_player_hp      = player.get("hp", self._prev_player_hp)
        self._prev_enemy_total_hp = self._sum_enemy_hp(state)

    @staticmethod
    def _sum_enemy_hp(state: dict) -> int:
        enemies = state.get("battle", {}).get("enemies", [])
        return sum(e.get("hp", 0) for e in enemies)
