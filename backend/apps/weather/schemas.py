from datetime import datetime

from pydantic import BaseModel


class WeatherFact(BaseModel):
    temp: int
    wind_speed: float
    pressure_mm: int


class WeatherRequest(BaseModel):
    fact: WeatherFact


class WeatherResponse(WeatherFact):
    pass


class CityWeather(WeatherFact):
    timestamp: float
