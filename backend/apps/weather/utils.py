import json
import os

from geopy import geocoders

from apps.weather.exceptions import GeoPosException
from apps.weather.schemas import CityWeather


def get_geo_pos(city: str) -> tuple:
    geolocator = geocoders.Nominatim(user_agent='telebot')  # FIXME
    geocode = geolocator.geocode(city)
    if not geocode:
        raise GeoPosException('Город не найден')
    latitude = geocode.latitude
    longitude = geocode.longitude
    return latitude, longitude


def write_file(path: str, city: str, values: CityWeather):
    data = read_file(path)
    data.update({city: values.model_dump()})

    with open(path, 'w+', encoding='utf-8') as file:
        json.dump(data, file)


def read_file(path: str):
    if os.path.isfile(path):
        with open(path, 'r') as file:
            read = file.read()
            data = json.loads(read)
            return data
    return {}
