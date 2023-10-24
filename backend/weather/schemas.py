from datetime import datetime

from pydantic import BaseModel


class WeatherFact(BaseModel):
    temp: int
    wind_speed: float
    pressure_mm: int


class WeatherData(BaseModel):
    fact: WeatherFact


class CityWeather(WeatherFact):
    timestamp: float