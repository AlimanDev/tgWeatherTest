from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from libraries.exceptions import YandexWeatherException
from weather.exceptions import GeoPosException
from weather.serializers import ParamsSerializer, ResultSerializer
from weather.services import get_weather_from_db, weather_save_to_db, fetch_weather, has_expired
from weather.utils import get_geo_pos


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
            request_weather = has_expired(weather['timestamp'], minute=30)

        if request_weather:
            try:
                lat, lon = get_geo_pos(city=city)
                weather_data = fetch_weather(lat, lon)
                weather = weather_save_to_db(city, weather_data)
            except (YandexWeatherException, GeoPosException) as e:
                success = 'error'
                message = str(e)

        result = {
            'success': success,
            'message': message,
            'data': weather
        }
        response = ResultSerializer(result)
        return Response(response.data, status=status.HTTP_200_OK)
