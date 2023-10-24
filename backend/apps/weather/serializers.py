from rest_framework import serializers


class CitySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)


class WeatherSerializer(serializers.Serializer):
    temp = serializers.IntegerField(default=0)
    wind_speed = serializers.FloatField(default=0)
    pressure_mm = serializers.IntegerField(default=0)


class ResultSerializer(serializers.Serializer):
    success = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    data = WeatherSerializer()
