import random
from collections import deque

from GameSim.Map.Encounter import Encounter

from CombatSim.Entities.Dungeon.Cultist import Cultist
from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Dungeon.GreenLouse import GreenLouse
from CombatSim.Entities.Dungeon.RedLouse import RedLouse
from CombatSim.Entities.Dungeon.SpikeSlimeMedium import SpikeSlimeMedium
from CombatSim.Entities.Dungeon.SpikeSlimeSmall import SpikeSlimeSmall
from CombatSim.Entities.Dungeon.SpikeSlimeLarge import SpikeSlimeLarge
from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Dungeon.AcidSlimeMedium import AcidSlimeMedium
from CombatSim.Entities.Dungeon.AcidSlimeLarge import AcidSlimeLarge
from CombatSim.Entities.Dungeon.FatGremlin import FatGremlin
from CombatSim.Entities.Dungeon.SneakyGremlin import SneakyGremlin
from CombatSim.Entities.Dungeon.MadGremlin import MadGremlin
from CombatSim.Entities.Dungeon.ShieldGremlin import ShieldGremlin
from CombatSim.Entities.Dungeon.WizardGremlin import WizardGremlin
from CombatSim.Entities.Dungeon.BlueSlaver import BlueSlaver
from CombatSim.Entities.Dungeon.RedSlaver import RedSlaver
from CombatSim.Entities.Dungeon.FungiBeast import FungiBeast
from CombatSim.Entities.Dungeon.Looter import Looter


def _make_louse(ascension, act):
    return random.choice([GreenLouse, RedLouse])(ascension=ascension, act=act)


def _cultist(asc, act):
    return [Cultist(ascension=asc, act=act)]


def _jaw_worm(asc, act):
    return [JawWorm(ascension=asc, act=act)]


def _two_louse(asc, act):
    return [_make_louse(asc, act), _make_louse(asc, act)]


def _small_slimes(asc, act):
    if random.random() < 0.5:
        return [SpikeSlimeMedium(ascension=asc, act=act), AcidSlimeSmall(ascension=asc, act=act)]
    else:
        return [AcidSlimeMedium(ascension=asc, act=act), SpikeSlimeSmall(ascension=asc, act=act)]


def _gang_of_gremlins(asc, act):
    pool = (
        [FatGremlin] * 2
        + [SneakyGremlin] * 2
        + [MadGremlin] * 2
        + [ShieldGremlin] * 1
        + [WizardGremlin] * 1
    )
    chosen = random.sample(pool, 4)
    return [cls(ascension=asc, act=act) for cls in chosen]


def _large_slime(asc, act):
    cls = random.choice([SpikeSlimeLarge, AcidSlimeLarge])
    return [cls(ascension=asc, act=act)]


def _swarm_of_slimes(asc, act):
    return (
        [SpikeSlimeSmall(ascension=asc, act=act) for _ in range(3)]
        + [AcidSlimeSmall(ascension=asc, act=act) for _ in range(2)]
    )


def _blue_slaver(asc, act):
    return [BlueSlaver(ascension=asc, act=act)]


def _red_slaver(asc, act):
    return [RedSlaver(ascension=asc, act=act)]


def _three_louse(asc, act):
    return [_make_louse(asc, act) for _ in range(3)]


def _two_fungi_beasts(asc, act):
    return [FungiBeast(ascension=asc, act=act), FungiBeast(ascension=asc, act=act)]


def _exordium_thugs(asc, act):
    first = random.choice([GreenLouse, AcidSlimeMedium])(ascension=asc, act=act)
    roll = random.random()
    if roll < 1/3:
        second = random.choice([BlueSlaver, RedSlaver])(ascension=asc, act=act)
    elif roll < 2/3:
        second = Cultist(ascension=asc, act=act)
    else:
        second = Looter(ascension=asc, act=act)
    return [first, second]


def _exordium_wildlife(asc, act):
    first = random.choice([FungiBeast, JawWorm])(ascension=asc, act=act)
    second = random.choice([GreenLouse, AcidSlimeMedium])(ascension=asc, act=act)
    return [first, second]


def _looter(asc, act):
    return [Looter(ascension=asc, act=act)]


EASY_POOL = [
    Encounter("Cultist", _cultist),
    Encounter("JawWorm", _jaw_worm),
    Encounter("2 Louse", _two_louse),
    Encounter("Small Slimes", _small_slimes),
]

HARD_POOL = [
    Encounter("Gang of Gremlins", _gang_of_gremlins),
    Encounter("Large Slime", _large_slime),
    Encounter("Swarm of Slimes", _swarm_of_slimes),
    Encounter("Blue Slaver", _blue_slaver),
    Encounter("Red Slaver", _red_slaver),
    Encounter("3 Louse", _three_louse),
    Encounter("2 Fungi Beasts", _two_fungi_beasts),
    Encounter("Exordium Thugs", _exordium_thugs),
    Encounter("Exordium Wildlife", _exordium_wildlife),
    Encounter("Looter", _looter),
]


class Act1EncounterPool:
    EASY_POOL_SIZE = 3  # first 3 monster encounters use Easy Pool

    def __init__(self):
        self.monster_encounter_count = 0
        self.recent_encounters = deque(maxlen=2)

    def get_next_encounter(self, ascension: int, act: int) -> list:
        pool = EASY_POOL if self.monster_encounter_count < self.EASY_POOL_SIZE else HARD_POOL
        candidates = [e for e in pool if e.name not in self.recent_encounters]
        if not candidates:
            candidates = pool  # fallback (shouldn't happen with pools of 4+)
        encounter = random.choice(candidates)
        self.recent_encounters.append(encounter.name)
        self.monster_encounter_count += 1
        print(f"[Encounter #{self.monster_encounter_count}] {encounter.name}")
        return encounter.create_enemies(ascension, act)
