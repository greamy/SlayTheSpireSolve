class EventOption:
    """
    One selectable option in an event menu.

    Usage — pass a bound method as `effect`:
        EventOption("Heal (35 gold)", "Restore 25% max HP.", self.heal)

    Or subclass EventOption and override apply() for more complex options.
    """

    def __init__(self, text: str, description: str = "", effect=None):
        self.text = text
        self.description = description
        self._effect = effect

    def apply(self, player):
        if self._effect is not None:
            self._effect(player)


class Event:
    """
    Base class for ? room events.

    Subclass this, set class-level `title` and `description`, and implement
    `build_options()` returning a list of EventOption objects.  Write the
    actual option logic as normal methods that accept `player`.

    Example
    -------
    class TheCleric(Event):
        title       = "The Cleric"
        description = "A wandering priest offers aid for a price."

        def build_options(self):
            return [
                EventOption("Heal (35 gold)", "Restore 25% of max HP.", self.heal),
                EventOption("Purify (50 gold)", "Remove a curse.", self.purify),
                EventOption("Leave", "", self.leave),
            ]

        def heal(self, player):
            player.heal(int(player.start_health * 0.25))
            player.gold -= 35

        def purify(self, player):
            player.gold -= 50
            # player.remove_curse(...)

        def leave(self, player):
            pass
    """

    title: str = "Unknown Event"
    description: str = ""

    def __init__(self, player, act, ascension):
        self.act = act
        self.ascension = ascension
        self.player = player
        self.options: list[EventOption] = self.build_options()
        self.chosen_option: int | None = None
        self.done: bool = False

    def build_options(self) -> list[EventOption]:
        raise NotImplementedError

    def apply(self, option_idx: int):
        """Apply the chosen option's effect."""
        if 0 <= option_idx < len(self.options):
            self.chosen_option = option_idx
            self.options[option_idx].apply(self.player)
            self.done = True


# ---------------------------------------------------------------------------
# Placeholder used until real events are added to the pool
# ---------------------------------------------------------------------------

class PlaceholderEvent(Event):
    title = "Mysterious Stranger"
    description = "A cloaked figure watches you from the shadows."

    def build_options(self):
        return [
            EventOption("Ignore them", "Nothing happens.", self.ignore),
            EventOption("Offer gold", "Lose 10 gold.", self.offer_gold),
            EventOption("Attack", "Take 5 damage.", self.attack),
        ]

    def ignore(self, player):
        pass

    def offer_gold(self, player):
        player.gold = max(0, player.gold - 10)

    def attack(self, player):
        player.take_damage(5)
