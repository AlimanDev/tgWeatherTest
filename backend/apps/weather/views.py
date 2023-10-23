from django.http import JsonResponse
from rest_framework.decorators import api_view

from apps.weather.schemas import WeatherResponse
from apps.weather.services import get_prev_weather, weather_save
from apps.weather.utils import geo_pos, weather


@api_view(['GET'])
def get_weather(request):
    """Возвращает погоду города"""

    if request.method == 'GET':
        city = request.GET.get('city')
        lat, lon = geo_pos(city=city)

        data = get_prev_weather(city)
        if not data:
            data = weather(lat, lon)
            weather_save(city, data)

        model_result = WeatherResponse.model_validate(data.fact.__dict__)
        return JsonResponse(model_result.model_dump())
