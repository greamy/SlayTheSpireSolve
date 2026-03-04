import random

from GameSim.Map.Event import Event, EventOption


class BigFish(Event):
    title = "Big Fish"
    description = (
        "You find a large fish flopping around on the ground. It opens its mouth "
        "and three items fall out."
    )

    def build_options(self):
        return [
            EventOption("Banana", "Heal 1/3 of your max HP.", self.banana),
            EventOption("Donut", "Gain 5 Max HP.", self.donut),
            EventOption("Box", "Obtain a relic. Become Cursed - Regret.", self.box),
            EventOption("Leave", ""),
        ]

    def banana(self, player):
        player.heal(player.start_health // 3)

    def donut(self, player):
        player.add_max_hp(5)

    def box(self, player):
        if not player.implemented_relics:
            return
        relic_name = random.choice(list(player.implemented_relics.keys()))
        cls = getattr(player.implemented_relics[relic_name], relic_name)
        player.add_relic(cls(player))
        player.add_card("Regret")