from abc import abstractmethod
from datetime import datetime

from django.conf import settings

from weather.schemas import YandexWeatherData
from weather.utils import JsonManager, YandexWeather


class WeatherRepository:
    @abstractmethod
    def save(self, data: dict):
        pass

    @abstractmethod
    def load(self) -> dict:
        pass


class WeatherRepositoryJson(WeatherRepository):
    def __init__(self, city):
        self.city = city
        self.json = JsonManager(settings.PATH_FILE)

    def save(self, data: dict):
        try:
            data_storage = self.json.read()
            mode = 'w+'
        except FileNotFoundError:
            data_storage = {}
            mode = 'w'

        data_storage.update({self.city: data})
        self.json.write(data=data_storage, mode=mode)

    def load(self) -> dict:
        self.json = JsonManager(settings.PATH_FILE)
        try:
            data = self.json.read()
            return data[self.city]
        except (KeyError, FileNotFoundError):
            return {}


def fetch_yandex_weather(lat: float, lon: float) -> YandexWeatherData:
    """Возвращает погоду по координатам"""

    endpoint = 'informers/'
    ya_weather = YandexWeather(lat=lat, lon=lon, token=settings.YANDEX_KEY)
    data = ya_weather.get_weather(endpoint)
    model = YandexWeatherData.model_validate(data)
    return model


def has_expired(data_in_timestamp: float, minute: int) -> bool:
    """Определяет срок годности данных"""

    expiry_time = minute * 60
    dt_now = datetime.now()
    dt_weather = datetime.fromtimestamp(data_in_timestamp)
    seconds_passed = (dt_now - dt_weather).seconds
    if seconds_passed > expiry_time:
        return True

    return False
