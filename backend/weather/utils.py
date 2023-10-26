import json

import requests
import urllib3
from geopy import geocoders
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from weather.exceptions import GeoPosException, YandexWeatherException

urllib3.disable_warnings()


class RequestAPI:
    def __init__(self, exception):
        self.exception = exception
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)

    def get(self, **kwargs):
        try:
            response = self.session.get(**kwargs)
            response.raise_for_status()
            data = response.json()
            return data
        except (
                requests.exceptions.RequestException,
                requests.exceptions.JSONDecodeError,
                KeyError,
        ) as e:
            raise self.exception(e)


class YandexWeather(RequestAPI):
    def __init__(self, lat: float, lon: float, token: str):
        super().__init__(exception=YandexWeatherException)
        self.api = 'https://api.weather.yandex.ru/v2/'
        self.params = {'lat': lat, 'lon': lon}
        self.header = {'X-Yandex-API-Key': token}

    def get_weather(self, endpoint: str) -> dict:
        """Возвращает данные о погоде"""

        data = self.get(url=self.api + endpoint, params=self.params, headers=self.header, verify=False)
        return data


class JsonManager:
    def __init__(self, filename: str):
        self.filename = filename

    def write(self, data: dict, mode: str = 'w'):
        with open(self.filename, mode=mode, encoding='utf-8') as file:
            json.dump(data, file)

    def read(self) -> dict:
        with open(self.filename, mode='r') as file:
            return json.loads(file.read())


def get_geo_pos(city: str) -> tuple:
    """Возвращает широту и долготу города"""

    geolocator = geocoders.Nominatim(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
    geocode = geolocator.geocode(city)
    if not geocode:
        raise GeoPosException('Город не найден')
    return geocode.latitude, geocode.longitude
