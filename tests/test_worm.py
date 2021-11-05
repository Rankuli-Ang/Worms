import unittest
from src.active_characters import worm
from resources.constants_values.common_types import Neighbors


class WormTest(unittest.TestCase):
    """General test class."""

    def test_strike(self) -> None:
        """Checks health change after strike."""
        self.first = worm.Worm((1, 1))
        self.second = worm.Worm((1, 1))

        control_health = self.second.get_health()
        control_health -= self.first.get_damage() * self.second.get_defense()
        self.first.strike(self.second)
        self.assertEqual(self.second.health, control_health)

    def test_move(self) -> None:
        """Checks not going out of borders of the field."""
        self.first = worm.Worm((1, 1))
        self.border_x = 3
        self.border_y = 3
        self.first.move((3, 3), self.border_x, self.border_y)
        self.assertEqual(self.first.coordinates, (2, 2))

    def test_safe_steps(self) -> None:
        """Checks the correctness of the danger assessment of steps."""
        self.control_worm = worm.Worm((10, 10))
        self.control_worm.health = 3
        self.danger_worm = worm.Worm((9, 10))
        self.danger_worm.health = 4
        self.equal_worm = worm.Worm((10, 9))
        self.equal_worm.health = 3

        self.steps = {Neighbors.UP: [self.danger_worm],
                      Neighbors.LEFT: [self.equal_worm],
                      Neighbors.RIGHT: []}
        result = self.control_worm.get_safe_steps(self.steps)
        self.assertNotIn((0, -1), result)
        self.assertIn((-1, 0), result)

    def test_deletion_mutation(self) -> None:
        """Checks the correctness of the deleting genes from genotype."""
        self.control_worm = worm.Worm((0, 0))
        test_genotype = worm.create_genome()
        self.control_worm.genetics.genotype = test_genotype
        rounds = 20
        while rounds > 0:
            self.control_worm.deletion_mutation()
            rounds -= 1
        self.assertEqual(len(self.control_worm.genetics.genotype), 0)


if __name__ == '__main__':
    unittest.main()
