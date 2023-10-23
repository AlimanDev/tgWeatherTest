from pydantic import BaseModel


class Result(BaseModel):
    temp: int
    wind_speed: float
    pressure_mm: int
