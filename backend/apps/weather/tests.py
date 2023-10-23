from datetime import datetime

from django.test import TestCase

from apps.weather.exceptions import GeoPosException
from apps.weather.schemas import CityWeather
from apps.weather.utils import geo_pos, JsonCRUD


class TestUtils(TestCase):

    def test_geo_pos(self):
        result = geo_pos(city='Ташкент')
        self.assertIsInstance(result, tuple)
        self.assertEquals(result, (41.3123363, 69.2787079))

    def test_raise_geo_pos(self):
        with self.assertRaises(GeoPosException):
            geo_pos(city='NotCity')


class TestJsonFile(TestCase):

    # def test_json_read(self):
    #     js = JsonCRUD()
    #     data = js.json_read()
    #     self.assertIsInstance(data, dict)

    def test_json_write(self):
        city_weather = CityWeather.model_validate({
            'timestamp': datetime.now().timestamp(),
            'temp': 1,
            'wind_speed': 1,
            'pressure_mm': 1
        })

        js = JsonCRUD()
        js.json_write(city='Бишкек', values=city_weather)

        city_weather = CityWeather.model_validate({
            'timestamp': datetime.now().timestamp(),
            'temp': 12,
            'wind_speed': 33,
            'pressure_mm': 22
        })
        js.json_write(city='Фергана', values=city_weather)


# class TestWeather(TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_weather(self):
#         weather()
