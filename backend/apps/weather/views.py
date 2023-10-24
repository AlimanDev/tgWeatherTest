from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.weather.exceptions import GeoPosException
from apps.weather.serializers import CitySerializer, ResultSerializer
from apps.weather.services import get_prev_weather_data, weather_save
from apps.weather.utils import geo_pos, weather
from libraries.exceptions import YandexWeatherException


class WeatherAPI(APIView):

    def get(self, request, *args, **kwargs):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        city = serializer.data['city']

        success = 'ok'
        message = 'ok'
        data = {  # Mock
            "temp": 12,
            "wind_speed": 1.3,
            "pressure_mm": 729
        }

        try:
            lat, lon = geo_pos(city=city)
            data = get_prev_weather_data(city)
            if not data:
                weather_data = weather(lat, lon)
                data = weather_save(city, weather_data)
        except (YandexWeatherException, GeoPosException) as e:
            success = 'error'
            message = str(e)

        response_data = {
            'success': success,
            'message': message,
            'data': data
        }
        result = ResultSerializer(data=response_data)
        result.is_valid(raise_exception=True)
        return Response(result.data, status=status.HTTP_200_OK)
