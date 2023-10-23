import json
import os

from geopy import geocoders

from apps.weather.exceptions import GeoPosException
from apps.weather.schemas import WeatherRequest, CityWeather
from conf import settings
from libraries.yandex_weather import Weather


def geo_pos(city: str) -> tuple:
    geolocator = geocoders.Nominatim(user_agent='telebot')  # FIXME
    geocode = geolocator.geocode(city)
    if not geocode:
        raise GeoPosException('Город не найден')
    latitude = geocode.latitude
    longitude = geocode.longitude
    return latitude, longitude


def weather(lat: float, lon: float) -> WeatherRequest:
    endpoint = 'informers/'
    data = Weather(
        lat=lat, lon=lon, token=settings.YANDEX_KEY
    ).get_weather(endpoint)
    model = WeatherRequest.model_validate(data)
    return model


class JsonCRUD:

    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def json_write(self, city: str, values: CityWeather):
        data = self.json_read()
        data.update({city: values.model_dump()})

        with open(self.path + self.filename, 'w+', encoding='utf-8') as file:
            json.dump(data, file)

    def json_read(self) -> dict:
        if os.path.isfile(self.path + self.filename):
            with open(self.path + self.filename, 'r') as file:
                read_file = file.read()
                data = json.loads(read_file)
                return data
        return {}
