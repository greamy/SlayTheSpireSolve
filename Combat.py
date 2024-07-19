from Player import Player
from Enemy import Enemy


class Combat:

    def __init__(self, player: Player, enemies: list):
        self.player = player

        if len(enemies) < 1:
            print("No enemies in combat")
        elif not isinstance(enemies[0], Enemy):
            print("Enemy list must contain Enemy objects")

        self.enemies = enemies

    def start(self):
        self.player.begin_combat()
        # TODO: Decide on intent of each enemy in the combat

        return self.run()

    def get_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def run(self):
        # Game loop of player turn -> Enemy turn until enemies or player is killed.
        num_turns = 0
        while self.player.health > 0 and self.get_enemy_health() > 0:
            self.player.start_turn()
            self.player.do_turn(self.enemies)

            for enemy in self.enemies:
                enemy.start_turn()
                enemy.do_turn(self.player)

            print(self.player)
            for enemy in self.enemies:
                print(enemy)

            num_turns += 1
        if self.player.health <= 0:
            print("YOU LOSE")
        if self.get_enemy_health() <= 0:
            print("YOU WIN")

        return num_turns, self.player.health, self.player.is_alive()




