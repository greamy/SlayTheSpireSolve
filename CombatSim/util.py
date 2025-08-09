import importlib

from matplotlib import pyplot as plt

from CombatSim.Entities.Player import Player
from GameSim.Input.RandomPlayerController import RandomPlayerController


def addCards(player, name_list: list[str]):
    cards = []
    for name in name_list:
        module = importlib.import_module("CombatSim.Actions.Library." + name)
        class_ = getattr(module, name)
        card = class_(player)
        cards.append(card)
    player.deck = Player.Deck(cards)


def createPlayer(lib_path='../CombatSim/Actions/Library', controller=RandomPlayerController(),
                 health=70, energy=3, gold=50, potions=None, relics=None, cards=None):
    if relics is None:
        relics = []
    if potions is None:
        potions = []
    if cards is None:
        cards = []
    return Player(health, energy, gold, potions, relics, cards, controller, lib_path)


def createEnemy(name: str, ascension: int, act: int):
    module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
    class_ = getattr(module, name)
    return class_(ascension, act)

def get_default_deck():
    cards = ["Strike" for _ in range(4)]
    cards.extend(["Defend" for _ in range(4)])
    cards.extend(["Vigilance", "Eruption"])
    # cards.extend(["Devotion" for _ in range(5)])
    # cards.extend(["SandsofTime" for _ in range(2)])
    return cards

def visualize_bot_comparison(simple_history, random_history):
    """
    Visualize the win rate comparison between simple bot and random bot

    Args:
        simple_history: Dict with enemy names as keys, [wins, total_combats] as values
        random_history: Dict with enemy names as keys, [wins, total_combats] as values
    """

    # Get all unique enemies from both histories
    all_enemies = set(simple_history.keys()) | set(random_history.keys())
    all_enemies = sorted(list(all_enemies))

    # Calculate win percentages for each bot
    simple_win_rates = []
    random_win_rates = []

    for enemy in all_enemies:
        # Simple bot win rate
        if enemy in simple_history:
            wins, total = simple_history[enemy]
            simple_rate = (wins / total) * 100 if total > 0 else 0
        else:
            simple_rate = 0
        simple_win_rates.append(simple_rate)

        # Random bot win rate
        if enemy in random_history:
            wins, total = random_history[enemy]
            random_rate = (wins / total) * 100 if total > 0 else 0
        else:
            random_rate = 0
        random_win_rates.append(random_rate)

    # Set up the bar chart
    x = np.arange(len(all_enemies))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create bars
    bars1 = ax.bar(x - width / 2, simple_win_rates, width, label='Simple Bot',
                   color='skyblue', alpha=0.8)
    bars2 = ax.bar(x + width / 2, random_win_rates, width, label='Random Bot',
                   color='lightcoral', alpha=0.8)

    # Add value labels on bars
    def add_value_labels(bars, values):
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', fontsize=8)

    add_value_labels(bars1, simple_win_rates)
    add_value_labels(bars2, random_win_rates)

    # Customize the chart
    ax.set_xlabel('Enemy Types', fontsize=12, fontweight='bold')
    ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Bot Performance Comparison: Win Rates Against Different Enemies',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(all_enemies, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 105)  # Set y-axis limit to show percentages clearly

    # Add overall statistics
    simple_overall = np.mean(simple_win_rates)
    random_overall = np.mean(random_win_rates)

    ax.text(0.02, 0.98, f'Simple Bot Average: {simple_overall:.1f}%\nRandom Bot Average: {random_overall:.1f}%',
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.show()