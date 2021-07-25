from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime, time, date


@dataclass
class TemperatureConfig:
    celsius: int
    fahrenheit: int


@dataclass
class WeatherConfig:
    feelslike: TemperatureConfig
    cloudcover: int
    humidity: int
    precip_inch: float
    precip_mm: float
    pressure_mbar: int
    pressure_inch: int
    temp: TemperatureConfig
    uv_index: int
    visibility_km: int
    visibility_mi: int
    weathercode: int
    winddirection_16point: str
    winddirection_deg: int
    windspeed_kmh: int
    windspeed_mph: int


@dataclass
class MoonConfig:
    illumination: int
    phase: str
    rise: time
    set: time


@dataclass
class SunConfig:
    rise: time
    set: time


@dataclass
class AstronomyConfig:
    moon: MoonConfig
    sun: SunConfig


@dataclass
class ChanceOfConfig:
    fog: int
    frost: int
    hightemp: int
    overcast: int
    rain: int
    remdry: int
    snow: int
    sunshine: int
    thunder: int
    windy: int


@dataclass
class HeatConfig:
    dewpoint: TemperatureConfig
    heatindex: TemperatureConfig
    windchill: TemperatureConfig


@dataclass
class HourlyConfig:
    heat: HeatConfig
    chanceof: ChanceOfConfig
    time: time
    description: str
    icon_url: str
    weather: WeatherConfig

    def __str__(self):
        return f"Weather at {self.time}"
    
    def _repr_pretty_(self, p, cycle):
        return p.text(str(self) if not cycle else '...')


@dataclass
class DailyConfig:
    astronomy: AstronomyConfig
    average: TemperatureConfig
    date: date
    hourly: List[HourlyConfig]
    temprange: Tuple[TemperatureConfig]
    sunhours: float
    totalsnow_cm: float
    uv_index: int

    def __str__(self):
        return f"Weather at {self.date}"
    
    def _repr_pretty_(self, p, cycle):
        return p.text(str(self) if not cycle else '...')


@dataclass
class CurrentConditionConfig:
    description: str
    icon_url: str
    weather: WeatherConfig
    obs_datetime_loc: datetime
    obs_time: time

    def __str__(self):
        return f"Current weather condition at {self.obs_datetime_loc}"
    
    def _repr_pretty_(self, p, cycle):
        return p.text(str(self) if not cycle else '...')


@dataclass
class NearestAreaConfig:
    name: str
    country: str
    lat: float
    lon: float
    population: int
    region: str
    weather_url: str


@dataclass
class RequestConfig:
    query: str
    type: str


@dataclass
class WeatherFileConfig:
    location: str
    current: CurrentConditionConfig
    nearest_area: NearestAreaConfig
    request: RequestConfig
    daily: List[DailyConfig]

    def __str__(self):
        return f"WeatherFile: {self.location}"
    
    def _repr_pretty_(self, p, cycle):
        return p.text(str(self) if not cycle else '...')
