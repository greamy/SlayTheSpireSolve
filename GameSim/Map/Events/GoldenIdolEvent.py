from CombatSim.Items.Relics.DisplayCase.GoldenIdol import GoldenIdol
from GameSim.Map.Event import Event, EventOption

_HIGH_ASCENSION = 15


class GoldenIdolEvent(Event):
    title = "Golden Idol"
    description = (
        "You enter a dusty tomb and find a golden idol sitting on a pedestal. "
        "It looks valuable, but taking it might trigger a trap..."
    )

    def __init__(self, player, act, ascension):
        self._took_idol = False
        super().__init__(player, act, ascension)

    def build_options(self):
        return [
            EventOption("Take", "Obtain Golden Idol. Trigger a trap.", self.take),
            EventOption("Leave", ""),
        ]

    def apply(self, option_idx: int):
        if not (0 <= option_idx < len(self.options)):
            return
        self.chosen_option = option_idx
        self.options[option_idx].apply(self.player)
        if self._took_idol:
            self._took_idol = False
            self.options = self._build_escape_options()
        else:
            self.done = True

    def take(self, player):
        player.add_relic(GoldenIdol(player))
        self._took_idol = True

    def _build_escape_options(self):
        smash_pct = 35 if self.ascension >= _HIGH_ASCENSION else 25
        hide_pct  = 10 if self.ascension >= _HIGH_ASCENSION else 8
        return [
            EventOption("Outrun", "Become Cursed - Injury.", self.outrun),
            EventOption(f"Smash", f"Take {smash_pct}% of max HP as damage.", self.smash),
            EventOption(f"Hide",  f"Lose {hide_pct}% of max HP permanently.", self.hide),
        ]

    def outrun(self, player):
        player.add_card("Injury")

    def smash(self, player):
        pct = 0.35 if self.ascension >= _HIGH_ASCENSION else 0.25
        player.take_damage(int(player.start_health * pct))

    def hide(self, player):
        pct = 0.10 if self.ascension >= _HIGH_ASCENSION else 0.08
        loss = int(player.start_health * pct)
        player.start_health -= loss
        player.health = min(player.health, player.start_health)

    def leave(self, player):
        pass
