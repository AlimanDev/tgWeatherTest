from enum import Enum

from pydantic import BaseModel


class Weather(BaseModel):
    temp: int
    wind_speed: float
    pressure_mm: int


class ResultSuccess(str, Enum):
    ok = 'ok'
    error = 'error'


class Result(BaseModel):
    success: ResultSuccess = ResultSuccess.ok
    message: str
    data: Weather
