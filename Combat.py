from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy


class Combat:

    def __init__(self, player: Player, enemies: list[Enemy], debug: bool):
        self.player = player

        if len(enemies) < 1:
            print("No enemies in combat")

        self.enemies = enemies
        self.debug = debug

    def start(self):
        self.player.begin_combat()
        return self.run()

    def get_total_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def run(self):
        # Game loop of player turn -> Enemy turn until enemies or player is killed.
        num_turns = 0
        while self.player.health > 0 and self.get_total_enemy_health() > 0:
            self.player.start_turn(self.enemies, self.debug)
            self.player.do_turn(self.enemies, self.debug)

            for enemy in self.enemies:
                enemy.start_turn([self.player], self.debug)
                enemy.do_turn(self.player, self.debug)

            if self.debug:
                print(self.player)
                for enemy in self.enemies:
                    print(enemy)

            num_turns += 1

        self.player.end_combat()
        if self.debug:
            if self.player.health <= 0:
                print("YOU LOSE")
            if self.get_total_enemy_health() <= 0:
                print("YOU WIN")

        return num_turns, self.player.health, self.player.is_alive()




