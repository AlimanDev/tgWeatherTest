from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.exceptions import GeoPosException
from weather.serializers import ParamsSerializer, ResultSerializer
from weather.services import get_weather_from_db, weather_save_to_db, get_weather, has_expired
from weather.utils import get_geo_pos
from libraries.exceptions import YandexWeatherException


class WeatherAPI(APIView):

    def get(self, request, *args, **kwargs):
        serializer = ParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        request_weather = True
        city = serializer.data['city']
        success = 'ok'
        message = 'ok'

        weather = get_weather_from_db(city)
        if weather:
            request_weather = has_expired(weather['timestamp'])

        if request_weather:
            try:
                lat, lon = get_geo_pos(city=city)
                weather_data = get_weather(lat, lon)
                weather = weather_save_to_db(city, weather_data)
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
