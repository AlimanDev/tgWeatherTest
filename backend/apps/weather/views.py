from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.weather.exceptions import GeoPosException
from apps.weather.serializers import CitySerializer, ResultSerializer
from apps.weather.services import get_prev_weather_data, weather_save, get_weather
from apps.weather.utils import get_geo_pos
from libraries.exceptions import YandexWeatherException


class WeatherAPI(APIView):

    def get(self, request, *args, **kwargs):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        city = serializer.data['city']
        success = 'ok'
        message = 'ok'
        weather = get_prev_weather_data(city)

        if not weather:
            try:
                lat, lon = get_geo_pos(city=city)
                weather_data = get_weather(lat, lon)
                weather = weather_save(city, weather_data)
            except (YandexWeatherException, GeoPosException) as e:
                success = 'error'
                message = str(e)

        response_data = {
            'success': success,
            'message': message,
            'data': weather
        }
        result = ResultSerializer(data=response_data)
        result.is_valid(raise_exception=True)
        return Response(result.data, status=status.HTTP_200_OK)
