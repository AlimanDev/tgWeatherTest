from datetime import datetime

from django.conf import settings

from apps.weather.schemas import CityWeather, WeatherRequest
from apps.weather.utils import JsonCRUD


js = JsonCRUD(f"{settings.BASE_DIR}/data/",  'cities.json')


def weather_save(city: str, data: WeatherRequest):
    city_weather = CityWeather.model_validate({
        'temp': data.fact.temp,
        'wind_speed': data.fact.wind_speed,
        'pressure_mm': data.fact.pressure_mm,
        'timestamp': datetime.now().timestamp(),
    })

    js.json_write(city, city_weather)


def get_prev_weather(city: str) -> dict | None:
    cities = js.json_read()
    if cities:
        if city in cities:
            city_data = cities[city]
            now = datetime.now()
            prev_now = datetime.fromtimestamp(city_data['timestamp'])
            timeout = (now - prev_now).seconds
            if timeout < 30 * 60:
                return city_data
    return None
