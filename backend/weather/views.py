from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.exceptions import GeoPosException
from weather.exceptions import YandexWeatherException
from weather.serializers import ParamsSerializer, ResultSerializer
from weather.services import fetch_yandex_weather, has_expired, WeatherRepositoryJson
from weather.utils import get_geo_pos


class WeatherAPI(APIView):

    def get(self, request, *args, **kwargs):
        serializer = ParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        need_request_weather = True
        city = serializer.data['city']
        result = {
            'success': 'ok',
            'message': 'ok',
            'data': {}
        }

        weather_repository = WeatherRepositoryJson(city=city)
        weather = weather_repository.load()
        if weather:
            need_request_weather = has_expired(weather['timestamp'], minute=30)

        if need_request_weather:
            try:
                lat, lon = get_geo_pos(city=city)
                weather_data = fetch_yandex_weather(lat, lon)
                weather = {
                    'temp': weather_data.fact.temp,
                    'wind_speed': weather_data.fact.wind_speed,
                    'pressure_mm': weather_data.fact.pressure_mm,
                    'timestamp': datetime.now().timestamp(),
                }
                weather_repository.save(data=weather)
            except (YandexWeatherException, GeoPosException) as e:
                result['success'] = 'error'
                result['message'] = str(e)

        result['data'] = weather
        response = ResultSerializer(result)
        return Response(response.data, status=status.HTTP_200_OK)
