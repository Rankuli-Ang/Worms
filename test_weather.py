import unittest
import weather


class TestWeather(unittest.TestCase):
    """General test class of module."""

    def test_upscaling(self) -> None:
        """Tests upscaling of weather objects."""

        weather_object = weather.Rain((0, 0))
        weather_object.set_side(5)
        weather_object.upscaling(3, 3)
        self.assertEqual(len(weather_object.all_coordinates), 15)
        self.assertEqual(max(weather_object.all_coordinates), (2, 2))


if __name__ == '__main__':
    unittest.main()
