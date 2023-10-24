from datetime import datetime

from django.conf import settings

from libraries.yandex_weather import YandexWeather
from weather.schemas import WeatherData
from weather.utils import write_file, read_file


def weather_save_to_db(city: str, data: WeatherData) -> dict:
    """Сохраняет данные о погоде"""

    mode = 'w'
    value = {
        'temp': data.fact.temp,
        'wind_speed': data.fact.wind_speed,
        'pressure_mm': data.fact.pressure_mm,
        'timestamp': datetime.now().timestamp(),
    }

    data = read_file(path=settings.PATH_FILE)
    if data:
        mode = 'w+'
    data.update({city: value})

    write_file(path=settings.PATH_FILE, data=data, mode=mode)

    return data


def get_weather_from_db(city: str) -> dict:
    """Возвращает данные о погоде города"""

    try:
        return read_file(settings.PATH_FILE)[city]
    except KeyError:
        return {}


def fetch_weather(lat: float, lon: float) -> WeatherData:
    """В погоду по координатам"""

    endpoint = 'informers/'
    data = YandexWeather(
        lat=lat, lon=lon, token=settings.YANDEX_KEY
    ).get_weather(endpoint)
    model = WeatherData.model_validate(data)
    return model


def has_expired(data_in_timestamp: float, minute: int) -> bool:
    """Определяет срок годности данных"""

    expiry_time = minute * 60
    dt_now = datetime.now()
    weather_dt = datetime.fromtimestamp(data_in_timestamp)
    seconds_passed = (dt_now - weather_dt).seconds
    if seconds_passed > expiry_time:
        return True

    return False
