from rest_framework import serializers


class CitySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)


class ResultSerializer(serializers.Serializer):
    temp = serializers.IntegerField(required=True)
    wind_speed = serializers.FloatField(required=True)
    pressure_mm = serializers.IntegerField(required=True)
