from pydantic import BaseModel


class WeatherFact(BaseModel):
    temp: int
    wind_speed: float
    pressure_mm: int


class YandexWeatherData(BaseModel):
    fact: WeatherFact
