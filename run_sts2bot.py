"""
STS2 Live Training Script

Runs the LSTMPPOAgent against the live Slay the Spire 2 game via the STS2MCP
HTTP API.  Requires:
  - STS2 running with the STS2MCP mod loaded (HTTP server on localhost:15526)
  - Game at the main menu before starting

Usage:
    python run_sts2bot.py [--load] [--no-train] [--character IRONCLAD]
"""

import argparse
import os
import sys
import time
from collections import deque

import numpy as np

# Make sure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from GameSim.Input.LSTM_PPO import LSTMPPOAgent
from Spire2Solve.gym_env.sts2_env import STS2Env

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
MODEL_DIR       = "artifacts/models/sts2live"
MODEL_PATH      = os.path.join(MODEL_DIR, "ppo_agent.pt")
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "ppo_agent_best.pt")

# ---------------------------------------------------------------------------
# Agent hyperparameters (mirror RLPlayerController)
# ---------------------------------------------------------------------------
ACTION_SPACE = {"BT": [10, 5, 1], "CB": 3}  # max_cards=10, max_enemies=5, other=1
CARD_VEC_LEN    = 19
PLAYER_VEC_LEN  = 11
ENEMY_VEC_LEN   = 12
STRAT_VEC_LEN   = 10


def build_state(obs: dict, deck: np.ndarray) -> dict:
    """
    Merge gymnasium observation dict with deck array into the state dict
    expected by LSTMPPOAgent._convert_state_to_tensors / embed_state.

    The deck may be empty if the hand is empty; pad to 1 row to avoid
    NaN in the AttentionStateEncoder mean-pool.
    """
    d = deck if deck.shape[0] > 0 else np.zeros((1, CARD_VEC_LEN), dtype=np.float32)
    return {
        "deck":        d,
        "hand":        obs["hand"],        # (10, 19)
        "player":      obs["player"],      # (11,)
        "strategic":   obs["strategic"],   # (10,)
        "enemies":     obs["enemies"],     # (5, 12)
        "action_mask": obs["action_mask"], # (51,) float32 — agent converts to bool
        "enemy_mask":  obs["enemy_mask"],  # (5,)  float32 — agent converts to bool
    }


def run_training(
    character:   str  = "IRONCLAD",
    num_episodes: int = 10_000,
    train:       bool = True,
    load_model:  bool = False,
    save_every:  int  = 50,
    max_steps:   int  = 800,
) -> None:

    os.makedirs(MODEL_DIR, exist_ok=True)

    # --- Environment ---
    env = STS2Env(character_id=character, max_steps=max_steps)

    # --- Agent ---
    agent = LSTMPPOAgent(
        num_actions           = ACTION_SPACE,
        card_feature_length   = CARD_VEC_LEN,
        player_feature_length = PLAYER_VEC_LEN,
        enemy_feature_length  = ENEMY_VEC_LEN,
        strategic_feature_length = STRAT_VEC_LEN,
        filepath              = MODEL_DIR,
        learning_enabled      = train,
        save_model            = train,
    )

    if load_model and os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH}")
        agent.load_models(MODEL_PATH)
    elif load_model:
        print(f"No model found at {MODEL_PATH}, starting fresh.")

    # --- Stats tracking ---
    ep_rewards    = deque(maxlen=100)
    ep_lengths    = deque(maxlen=100)
    win_history   = deque(maxlen=100)  # 1=survived to next floor / run end, 0=died
    best_avg_reward = float("-inf")

    print(f"\n{'='*60}")
    print(f"  STS2 Live Training — {character}")
    print(f"  Episodes: {num_episodes}  |  Train: {train}  |  Max steps/ep: {max_steps}")
    print(f"  Model dir: {MODEL_DIR}")
    print(f"{'='*60}\n")
    print("Make sure STS2 is open at the main menu with the mod loaded.")
    print("Press Ctrl-C to stop and save.\n")

    for episode in range(1, num_episodes + 1):
        ep_start = time.time()

        # ---- Reset ----
        obs, info = env.reset()
        agent.reset_hidden_state()

        state      = build_state(obs, info["deck"])
        state_t    = agent._convert_state_to_tensors(state)
        action, log_prob, value, _ = agent.choose_action(state_t)

        ep_reward = 0.0
        step      = 0
        done      = False

        # ---- Episode loop ----
        while not done:
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_reward += reward
            step      += 1

            new_state = build_state(obs, info["deck"])

            # agent.step stores the transition and (if enough data) triggers _learn()
            # It returns the next action to take in new_state.
            action, log_prob, value, _ = agent.step(
                prev_state   = state,
                action_taken = action,
                log_prob     = log_prob,
                reward       = reward,
                done         = done,
                new_state    = new_state,
                value        = value,
            )

            state = new_state

        # ---- Episode stats ----
        ep_rewards.append(ep_reward)
        ep_lengths.append(step)
        survived = 1 if info.get("state_type") != "game_over" and obs["player"][0] > 0 else 0
        win_history.append(survived)

        elapsed  = time.time() - ep_start
        avg_rew  = sum(ep_rewards)  / len(ep_rewards)
        avg_len  = sum(ep_lengths)  / len(ep_lengths)
        win_rate = sum(win_history) / len(win_history) * 100

        print(
            f"Ep {episode:5d} | "
            f"reward {ep_reward:+7.3f} | "
            f"avg100 {avg_rew:+7.3f} | "
            f"steps {step:4d} | "
            f"win% {win_rate:5.1f} | "
            f"{elapsed:.1f}s"
        )

        # ---- Periodic checkpoint ----
        if train and episode % save_every == 0:
            agent.save_models(MODEL_PATH)
            print(f"  [checkpoint] saved to {MODEL_PATH}")

        # ---- Best-reward checkpoint ----
        if train and avg_rew > best_avg_reward and len(ep_rewards) >= 10:
            best_avg_reward = avg_rew
            agent.save_models(BEST_MODEL_PATH)
            print(f"  [best] new best avg reward {avg_rew:.3f} — saved to {BEST_MODEL_PATH}")

    # ---- Final save ----
    if train:
        agent.save_models(MODEL_PATH)
        print(f"\nTraining complete. Final model saved to {MODEL_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train LSTMPPOAgent on live STS2")
    parser.add_argument("--character", default="IRONCLAD",
                        help="Character ID to play (default: IRONCLAD)")
    parser.add_argument("--episodes", type=int, default=10_000,
                        help="Number of episodes to run (default: 10000)")
    parser.add_argument("--load", action="store_true",
                        help="Load existing model from MODEL_PATH before training")
    parser.add_argument("--no-train", action="store_true",
                        help="Disable learning (inference / benchmark mode)")
    parser.add_argument("--save-every", type=int, default=50,
                        help="Save checkpoint every N episodes (default: 50)")
    parser.add_argument("--max-steps", type=int, default=800,
                        help="Max env steps per episode before truncation (default: 800)")
    args = parser.parse_args()

    try:
        run_training(
            character    = args.character,
            num_episodes = args.episodes,
            train        = not args.no_train,
            load_model   = args.load,
            save_every   = args.save_every,
            max_steps    = args.max_steps,
        )
    except KeyboardInterrupt:
        print("\nInterrupted by user.")


if __name__ == "__main__":
    main()
