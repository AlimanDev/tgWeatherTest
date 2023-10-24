from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from libraries.yandex_weather import YandexWeather
from weather.exceptions import GeoPosException
from weather.schemas import WeatherData
from weather.services import has_expired, fetch_weather
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
        with patch('weather.views.get_weather_from_db', return_value=get_weather_from_db_return):
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

    @patch.object(YandexWeather, 'query')
    def test_fetch_weather(self, mock_post):
        fake_result_success = {
            'fact': {
                'temp': 0,
                'wind_speed': 0,
                'pressure_mm': 0,
            }
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value = fake_result_success

        result = fetch_weather(0, 0)
        data = WeatherData.model_validate(fake_result_success)
        self.assertIsInstance(result, WeatherData)
        self.assertEquals(result, data)
