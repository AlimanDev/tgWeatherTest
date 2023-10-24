import json
import os

from geopy import geocoders

from weather.exceptions import GeoPosException


def get_geo_pos(city: str) -> tuple:
    """Возвращает широту и долготу города"""

    geolocator = geocoders.Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
    geocode = geolocator.geocode(city)
    if not geocode:
        raise GeoPosException('Город не найден')
    latitude = geocode.latitude
    longitude = geocode.longitude

    return latitude, longitude


def write_file(path: str, data: dict, mode: str = 'w'):
    """Запись в файл"""

    with open(path, mode=mode, encoding='utf-8') as file:
        json.dump(data, file)


def read_file(path: str):
    """Чтение файла"""

    if os.path.isfile(path):
        with open(path, mode='r') as file:
            read = file.read()
            data = json.loads(read)
            return data
    return {}
