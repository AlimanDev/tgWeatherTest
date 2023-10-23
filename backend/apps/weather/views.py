from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view

from apps.weather.utils import geo_pos
from libraries.yandex_weather import Weather
from apps.weather.schemas import WeatherRequest, WeatherResponse


@api_view(['GET'])
def get_weather(request):
    """
    Возвращает погоду города
    """
    if request.method == 'GET':
        city = request.GET.get('city')
        lat, lon = geo_pos(city=city)
        endpoint = 'informers/'
        data = Weather(
            lat=lat, lon=lon, token=settings.YANDEX_KEY
        ).get_weather(endpoint)
        model_request = WeatherRequest.model_validate(data)
        model_result = WeatherResponse.model_validate(model_request.fact.__dict__)
        print(model_result.model_dump())
        return JsonResponse(model_result.model_dump())
