from django.test import TestCase

from apps.weather.exceptions import GeoPosException
from apps.weather.utils import geo_pos


class TestUtils(TestCase):

    def test_geo_pos(self):
        result = geo_pos(city='Ташкент')
        self.assertIsInstance(result, tuple)
        self.assertEquals(result, (41.3123363, 69.2787079))

    def test_raise_geo_pos(self):
        with self.assertRaises(GeoPosException):
            geo_pos(city='asdasdasd')
