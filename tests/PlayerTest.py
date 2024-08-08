import unittest
from CombatSim.Entities.Player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.player = Player(self.health, self.energy, self.gold, [], [], [])

        self.damage = 10
        self.block = 10
        self.debug = False

    def test_gain_block(self):
        self.player.gain_block(self.block, [None], self.debug)
        self.assertEqual(self.player.block, self.block)

        self.player.gain_block(self.block, [None], self.debug)
        self.assertEqual(self.player.block, self.block * 2)

    def test_take_damage(self):
        self.player.take_damage(self.damage)
        self.assertEqual(self.player.health, self.health-self.damage)

    def test_take_damage_block(self):
        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage/2)
        self.assertEqual(self.player.health, self.health)
        self.assertEqual(self.player.block, self.block/2)

        self.player.block = 0

        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage)
        self.assertEqual(self.player.health, self.health)
        self.assertEqual(self.player.block, 0)

        self.player.block = 0

        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage*2)
        self.assertEqual(self.player.health, self.health-self.damage)
        self.assertEqual(self.player.block, 0)

    def test_take_damage_wrath(self):
        self.player.set_stance(Player.Stance.WRATH)
        self.player.take_damage(self.damage)
        self.assertEqual(self.player.health, self.health - (self.damage*2))

    def test_take_damage_wrath_block(self):
        self.player.set_stance(Player.Stance.WRATH)

        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage/5)
        self.assertEqual(self.player.health, self.health)
        self.assertEqual(self.player.block, 6)

        self.player.block = 0

        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage/2)
        self.assertEqual(self.player.health, self.health)
        self.assertEqual(self.player.block, 0)

        self.player.block = 0
        self.player.gain_block(self.block, [None], self.debug)
        self.player.take_damage(self.damage)
        self.assertEqual(self.player.health, self.health-self.damage)
        self.assertEqual(self.player.block, 0)


if __name__ == '__main__':
    unittest.main()
