import random

# Cards excluded from combat reward pools (basic, status, generated, curses)
_SPECIAL_CARDS = {
    # Basic cards
    'Strike', 'Defend',
    # Status cards
    'Slimed', 'Wound', 'Dazed', 'Miracle', 'Burn',
    # Generated mid-combat cards
    'Beta', 'Omega', 'Expunger', 'Insight', 'Smite', 'Indignation',
    # Curses
    'CurseoftheBell', 'Injury', 'Decay', 'Pain', 'Regret',
}

_RARE_CARDS = {
    'Alpha', 'Blasphemy', 'Brilliance', 'ConjureBlade', 'DeusExMachina',
    'DevaForm', 'Devotion', 'Establishment', 'ForeignInfluence', 'Judgment',
    'LessonLearned', 'MasterReality', 'Omniscience', 'Ragnarok', 'ReachHeaven',
    'SignatureMove', 'SimmeringFury', 'Study', 'ThroughViolence', 'Vault', 'Wish',
}

_UNCOMMON_CARDS = {
    'BattleHymn', 'BowlingBash', 'CarveReality', 'Collect', 'Crescendo',
    'CrushJoints', 'CutThroughFate', 'DeceiveReality', 'EmptyMind', 'Fasting',
    'FearNoEvil', 'FlurryofBlows', 'FollowUp', 'Foresight', 'InnerPeace',
    'LikeWater', 'Meditate', 'MentalFortress', 'Nirvana', 'Perseverance',
    'Pray', 'Rushdown', 'Sanctity', 'SandsofTime', 'SashWhip', 'Scrawl',
    'SpiritShield', 'Swivel', 'TalktotheHand', 'Tantrum', 'ThirdEye', 'Wallop',
    'WaveoftheHand', 'Weave', 'WheelKick', 'WindmillStrike', 'WreathofFlame',
}

_COMMON_CARDS = {
    'Conclude', 'Consecrate', 'EmptyBody', 'EmptyFist', 'Eruption',
    'Evaluate', 'FlyingSleeves', 'Halt', 'JustLucky', 'PressurePoints',
    'Prostrate', 'Protect', 'Safety', 'Tranquility', 'Vigilance', 'Worship',
}


def generate_card_reward(player, is_elite: bool) -> list:
    """
    Generate 3 card reward options after combat.

    Rarity chances (before offset):
      Normal combat: Rare 3%, Uncommon 37%, Common 60%
      Elite combat:  Rare 10%, Uncommon 40%, Common 50%

    player.rare_chance_offset starts at -5, increases +1 per common roll,
    resets to -5 on any rare roll, capped at +40.
    """
    card_pools = {'common': [], 'uncommon': [], 'rare': []}
    for card_name in player.implemented_cards:
        if card_name in _RARE_CARDS:
            card_pools['rare'].append(card_name)
        elif card_name in _UNCOMMON_CARDS:
            card_pools['uncommon'].append(card_name)
        elif card_name in _COMMON_CARDS:
            card_pools['common'].append(card_name)

    base_rare = 10 if is_elite else 3
    base_uncommon = 40 if is_elite else 37

    chosen = []
    for _ in range(3):
        card_name = _roll_card(player, card_pools, base_rare, base_uncommon, chosen)
        if card_name is not None:
            chosen.append(card_name)
    return chosen


def _roll_card(player, card_pools, base_rare, base_uncommon, exclude):
    offset = player.rare_chance_offset
    effective_rare = base_rare + offset

    # Negative rare chance bleeds into uncommon
    if effective_rare < 0:
        effective_uncommon = max(0, base_uncommon + effective_rare)
        effective_rare = 0
    else:
        effective_uncommon = base_uncommon

    roll = random.random() * 100

    if roll < effective_rare:
        rolled_rarity = 'rare'
        player.rare_chance_offset = -5
    elif roll < effective_rare + effective_uncommon:
        rolled_rarity = 'uncommon'
    else:
        rolled_rarity = 'common'
        player.rare_chance_offset = min(player.rare_chance_offset + 1, 40)

    pool = [c for c in card_pools[rolled_rarity] if c not in exclude]
    if not pool:
        for fallback in ('uncommon', 'common', 'rare'):
            if fallback != rolled_rarity:
                pool = [c for c in card_pools[fallback] if c not in exclude]
                if pool:
                    break

    return random.choice(pool) if pool else None