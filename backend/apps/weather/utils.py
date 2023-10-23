from geopy import geocoders

from apps.weather.exceptions import GeoPosException


def geo_pos(city: str) -> tuple:
    geolocator = geocoders.Nominatim(user_agent='telebot')  # FIXME: разобрать что это
    geocode = geolocator.geocode(city)
    if not geocode:
        raise GeoPosException('Город не найден')
    latitude = geocode.latitude
    longitude = geocode.longitude
    return latitude, longitude
