from datetime import datetime

from django.test import TestCase

from weather.exceptions import GeoPosException
from weather.schemas import CityWeather
from weather.utils import get_geo_pos, JsonCRUD


class TestUtils(TestCase):

    def test_geo_pos(self):
        result = get_geo_pos(city='Ташкент')
        self.assertIsInstance(result, tuple)
        self.assertEquals(result, (41.3123363, 69.2787079))

    def test_raise_geo_pos(self):
        with self.assertRaises(GeoPosException):
            get_geo_pos(city='NotCity')