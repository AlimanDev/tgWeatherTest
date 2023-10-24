from datetime import datetime, timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from weather.exceptions import GeoPosException
from weather.services import has_expired
from weather.utils import get_geo_pos


class WeatherAPIViewTest(TestCase):

    def test_api(self):
        data = {
            'temp': 0,
            'wind_speed': 0,
            'pressure_mm': 0,
        }
        get_weather_from_db_return = {
            'timestamp': datetime.now().timestamp()
        }
        get_weather_from_db_return.update(data)
        with mock.patch('weather.views.get_weather_from_db', return_value=get_weather_from_db_return):
            url = "%s?city=Tashkent" % reverse('weather')
            result = {'success': 'ok', 'message': 'ok', 'data': data}
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.json(), result)


class UtilsTest(TestCase):

    def test_geo_pos(self):
        result = get_geo_pos(city='Ташкент')
        self.assertIsInstance(result, tuple)
        self.assertEquals(result, (41.3123363, 69.2787079))

    def test_raise_geo_pos(self):
        with self.assertRaises(GeoPosException):
            get_geo_pos(city='NotCity')


class ServicesTest(TestCase):

    def test_expired(self):
        minute = 30
        dt_now = has_expired(datetime.now().timestamp(), minute)
        expired_dt_now = has_expired((datetime.now() - timedelta(minutes=31)).timestamp(), minute)
        self.assertEqual(expired_dt_now, True)
        self.assertEqual(dt_now, False)
