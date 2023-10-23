import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from apps.libraries.exceptions import YandexWeatherException


class Weather:
    def __init__(self, lat: float, lon: float, token: str):
        self.url = 'https://api.weather.yandex.ru/v2/'
        self.params = {
            'lat': lat,
            'long': lon,
            'lang': 'ru_Ru'
        }
        self.lat = lat
        self.lon = lon
        self.header = {'X-Yandex-API-Key': token}
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)

    def get_weather(self, endpoint: str):
        data = self.query(url=self.url + endpoint)
        return data

    def query(self, url: str) -> dict:
        """Возвращает результат запроса."""

        try:
            response = self.session.get(
                url=url,
                params=self.params,
                headers=self.header,
                verify=False
            )
            response.raise_for_status()
            data = response.json()
            return data
        except (
                requests.exceptions.RequestException,
                requests.exceptions.JSONDecodeError,
                KeyError,
        ) as e:
            raise YandexWeatherException(e)