import random

from CombatSim.Items.Relics.DisplayCase.CultistHeadpiece import CultistHeadpiece
from CombatSim.Items.Relics.DisplayCase.FaceOfCleric import FaceOfCleric
from CombatSim.Items.Relics.DisplayCase.GremlinVisage import GremlinVisage
from CombatSim.Items.Relics.DisplayCase.NlothsHungryFace import NlothsHungryFace
from CombatSim.Items.Relics.DisplayCase.SsserpentHead import SsserpentHead
from GameSim.Map.Event import Event, EventOption

_TOUCH_GOLD = 75
_TOUCH_GOLD_HIGH_ASCENSION = 50
_TOUCH_DAMAGE_PCT = 0.10
_HIGH_ASCENSION = 15

# Weighted face pool: 40% good, 40% bad, 20% neutral
_FACE_POOL = [
    FaceOfCleric,
    SsserpentHead,
    GremlinVisage,
    NlothsHungryFace,
    CultistHeadpiece,
]
_FACE_WEIGHTS = [0.20, 0.20, 0.20, 0.20, 0.20]


class FaceTrader(Event):
    title = "Face Trader"
    description = (
        "You stumble upon a curious merchant with a table full of strange masks. "
        "'Wanna trade? I'll give you something good for that face of yours!'"
    )

    def build_options(self):
        return [
            EventOption("Touch", f"Lose 10% max HP. Gain {_TOUCH_GOLD} gold.", self.touch),
            EventOption("Trade", "Give your face. Receive a random mask relic.", self.trade),
            EventOption("Leave", ""),
        ]

    def touch(self, player):
        damage = max(1, int(player.start_health * _TOUCH_DAMAGE_PCT))
        player.take_damage(damage)
        gold = _TOUCH_GOLD_HIGH_ASCENSION if self.ascension >= _HIGH_ASCENSION else _TOUCH_GOLD
        player.gold += gold

    def trade(self, player):
        face_cls = random.choices(_FACE_POOL, weights=_FACE_WEIGHTS, k=1)[0]
        player.add_relic(face_cls(player))

    def leave(self, player):
        pass