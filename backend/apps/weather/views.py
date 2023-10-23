from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.weather.serializers import CitySerializer, ResultSerializer
from apps.weather.services import get_prev_weather, weather_save
from apps.weather.utils import geo_pos, weather


class WeatherAPI(APIView):

    def get(self, request, *args, **kwargs):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        city = serializer.data['city']

        # lat, lon = geo_pos(city=city)
        # data = get_prev_weather(city)
        # if not data:
        #     req = weather(lat, lon)
        #     data = weather_save(city, req)
        # Mock
        data = {
            "temp": 12,
            "wind_speed": 1.3,
            "pressure_mm": 729
        }

        result = ResultSerializer(data=data)
        result.is_valid(raise_exception=True)
        return Response(result.data, status=status.HTTP_200_OK)
