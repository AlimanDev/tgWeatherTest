from datetime import datetime

from django.conf import settings

from apps.weather.schemas import CityWeather, WeatherRequest
from apps.weather.utils import write_file, read_file


def weather_save(city: str, data: WeatherRequest) -> dict:
    data = {
        'temp': data.fact.temp,
        'wind_speed': data.fact.wind_speed,
        'pressure_mm': data.fact.pressure_mm,
        'timestamp': datetime.now().timestamp(),
    }
    city_weather = CityWeather.model_validate(data)
    write_file(settings.PATH_FILE, city, city_weather)

    return data


def get_prev_weather_data(city: str) -> dict:
    cities = read_file(settings.PATH_FILE)
    if cities:
        if city in cities:
            city_data = cities[city]
            now = datetime.now()
            prev_now = datetime.fromtimestamp(city_data['timestamp'])
            timeout = (now - prev_now).seconds
            if timeout < 30 * 60:
                return city_data
    return {}
