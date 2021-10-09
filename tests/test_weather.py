import unittest
from . import weather
from . import worm


class TestWeather(unittest.TestCase):
    """General test class of module."""

    def test_upscaling(self) -> None:
        """Checks upscaling of weather objects."""

        weather_object = weather.Rain((0, 0))
        weather_object.side = 5
        weather_object.upscaling(3, 3)
        self.assertEqual(len(weather_object.all_coordinates), 15)
        self.assertEqual(max(weather_object.all_coordinates), (2, 2))

    def test_tornado_effect(self) -> None:
        """Checks scattering worms and food objects."""
        tornado = weather.Tornado((3, 3))
        border_x = 5
        border_y = 5

        foods = []
        food_object = worm.Food((3, 3))
        foods.append(food_object)

        worms = []
        worm_object = worm.Worm((3, 3))
        worms.append(worm_object)

        result_coordinates_variations = [(0, 3), (3, 0), (4, 3), (3, 4)]

        tornado.tornado_effect(worms, foods, border_x, border_y)
        self.assertIn(worm_object.coordinates, result_coordinates_variations)
        self.assertIn(food_object.coordinates, result_coordinates_variations)


if __name__ == '__main__':
    unittest.main()
