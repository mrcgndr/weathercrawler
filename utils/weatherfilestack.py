import pandas as pd
import json
import os
from datetime import datetime, timedelta
from flatten_dict import flatten
from glob import glob
from tqdm import tqdm
from p_tqdm import p_map
from typing import Union

from .config import *


def _validate_date(string: str, format: str) -> bool:
    try:
        datetime.strptime(string, format)
        return True
    except ValueError:
        return False


def _strptime(string: str, format: str, ret_type: str) -> Union[datetime, datetime.time, datetime.date, None]:
    assert ret_type in ["date", "time", "datetime"]
    if _validate_date(string, format): 
        d = datetime.strptime(string, format)
        if ret_type == "date":
            return d.date()
        elif ret_type == "time":
            return d.time()
        elif ret_type == "datetime":
            return d 
    else:
        return None


def _daterange(start: datetime.date, end: datetime.date) -> List[datetime.date]:
    return [start + timedelta(days=x) for x in range(0, (end-start).days)]


def parse_weatherfile(filepath: str, location: str) -> WeatherFileConfig:
    with open(filepath, "r") as f:
        json_dict = json.load(f) 
    
    try:
        current = json_dict["current_condition"][0]
        nearest = json_dict["nearest_area"][0]
        weather = [d for d in json_dict["weather"]]

        w = WeatherFileConfig(
            location = location,
            current = CurrentConditionConfig(
                description = current["weatherDesc"][0]["value"],
                icon_url = current["weatherIconUrl"][0]["value"],
                weather = WeatherConfig(
                    feelslike = TemperatureConfig(
                        celsius = int(current["FeelsLikeC"]),
                        fahrenheit = int(current["FeelsLikeF"])
                    ),
                    cloudcover = int(current["cloudcover"]),
                    humidity = int(current["humidity"]),
                    precip_inch = float(current["precipInches"]) if "precipInches" in current.keys() else None,
                    precip_mm = float(current["precipMM"]),
                    pressure_mbar = int(current["pressure"]),
                    pressure_inch = int(current["pressureInches"]) if "pressureInches" in current.keys() else None,
                    temp = TemperatureConfig(
                        celsius = int(current["temp_C"]),
                        fahrenheit = int(current["temp_F"])
                    ),
                    uv_index = int(current["uvIndex"]),
                    visibility_km = int(current["visibility"]),
                    visibility_mi = int(current["visibilityMiles"]) if "visibilityMiles" in current.keys() else None,
                    weathercode = int(current["weatherCode"]),
                    winddirection_16point = current["winddir16Point"],
                    winddirection_deg = int(current["winddirDegree"]),
                    windspeed_kmh = int(current["windspeedKmph"]),
                    windspeed_mph = int(current["windspeedMiles"])
                ),
                obs_datetime_loc = _strptime(current["localObsDateTime"], "%Y-%m-%d %I:%M %p", "datetime"),
                obs_time = _strptime(current["observation_time"], "%I:%M %p", "time")
            ),
            nearest_area = NearestAreaConfig(
                name = nearest["areaName"][0]["value"],
                country = nearest["country"][0]["value"],
                lon = float(nearest["longitude"]),
                lat = float(nearest["latitude"]),
                population = int(nearest["population"]) if "population" in nearest.keys() else None,
                region = nearest["region"][0]["value"],
                weather_url = nearest["weatherUrl"][0]["value"] if "weatherUrl" in nearest.keys() else None
            ),
            request = RequestConfig(
                query = json_dict["request"][0]["query"],
                type = json_dict["request"][0]["type"]
            ),
            daily = [
                DailyConfig(
                    astronomy = AstronomyConfig(
                        moon = MoonConfig(
                            illumination = int(w["astronomy"][0]["moon_illumination"]),
                            phase = w["astronomy"][0]["moon_phase"],
                            rise = _strptime(w["astronomy"][0]["moonrise"], "%I:%M %p", "time"),
                            set = _strptime(w["astronomy"][0]["moonset"], "%I:%M %p", "time")
                        ),
                        sun = SunConfig(
                            rise = _strptime(w["astronomy"][0]["sunrise"], "%I:%M %p", "time"),
                            set = _strptime(w["astronomy"][0]["sunset"], "%I:%M %p", "time")
                        )
                    ),
                    average = TemperatureConfig(
                        celsius = int(w["avgtempC"]) if "avgtempC" in w.keys() else None,
                        fahrenheit = int(w["avgtempF"]) if "avgtempF" in w.keys() else None
                    ),
                    date = _strptime(w["date"], "%Y-%m-%d", "date"),
                    hourly = [
                        HourlyConfig(
                            heat = HeatConfig(
                                dewpoint = TemperatureConfig(
                                    celsius = int(h["DewPointC"]),
                                    fahrenheit = int(h["DewPointF"])
                                ),
                                heatindex = TemperatureConfig(
                                    celsius = int(h["HeatIndexC"]),
                                    fahrenheit = int(h["HeatIndexF"])
                                ),
                                windchill = TemperatureConfig(
                                    celsius = int(h["WindChillC"]),
                                    fahrenheit = int(h["WindChillF"]) 
                                )
                            ),
                            chanceof = ChanceOfConfig(
                                fog = int(h["chanceoffog"]),
                                frost = int(h["chanceoffrost"]),
                                hightemp = int(h["chanceofhightemp"]),
                                overcast = int(h["chanceofovercast"]),
                                rain = int(h["chanceofrain"]),
                                remdry = int(h["chanceofremdry"]),
                                snow = int(h["chanceofsnow"]),
                                sunshine = int(h["chanceofsunshine"]),
                                thunder = int(h["chanceofthunder"]),
                                windy = int(h["chanceofwindy"])
                            ),
                            time = _strptime(f"{int(h['time']):04g}", "%H%M", "time"),
                            description = h["weatherDesc"][0]["value"],
                            icon_url = h["weatherIconUrl"][0]["value"],
                            weather = WeatherConfig(
                                feelslike = TemperatureConfig(
                                    celsius = int(h["FeelsLikeC"]),
                                    fahrenheit = int(h["FeelsLikeF"])
                                ),
                                cloudcover = int(h["cloudcover"]),
                                humidity = int(h["humidity"]),
                                precip_inch = float(h["precipInches"]) if "precipInches" in h.keys() else None,
                                precip_mm = float(h["precipMM"]),
                                pressure_mbar = int(h["pressure"]),
                                pressure_inch = int(h["pressureInches"]) if "pressureIncehs" in h.keys() else None,
                                temp = TemperatureConfig(
                                    celsius = int(h["tempC"]),
                                    fahrenheit = int(h["tempF"])
                                ),
                                uv_index = int(h["uvIndex"]),
                                visibility_km = int(h["visibility"]),
                                visibility_mi = int(h["visibilityMiles"]) if "visibilityMiles" in h.keys() else None,
                                weathercode = int(h["weatherCode"]),
                                winddirection_16point = h["winddir16Point"],
                                winddirection_deg = int(h["winddirDegree"]),
                                windspeed_kmh = int(h["windspeedKmph"]),
                                windspeed_mph =int(h["windspeedMiles"])
                            )
                        )
                    for h in w["hourly"]],
                    temprange = (
                        TemperatureConfig(
                            celsius = int(w["mintempC"]),
                            fahrenheit = int(w["mintempF"])
                        ),
                        TemperatureConfig(
                            celsius = int(w["maxtempC"]),
                            fahrenheit = int(w["maxtempF"])
                        )
                    ),
                    sunhours = float(w["sunHour"]),
                    totalsnow_cm = float(w["totalSnow_cm"]),
                    uv_index = int(w["uvIndex"])
                )
            for w in weather]
        )

        return w
    
    except Exception as e:
        print(f"File {filepath} could not be parsed. Error: {e}")

class WeatherFileStack():

    def __init__(self,
                 file_dir: str,
                 location: str,
                 start_date: str = None,
                 end_date: str = None,
                 n_workers: int = 1):
        if start_date:
            assert _validate_date(start_date, "%Y-%m-%d"), "start_date should have the format '%Y-%m-%d'."
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            self.start_date = None
        if end_date:
            assert _validate_date(end_date, "%Y-%m-%d"), "end_date should have the format '%Y-%m-%d'."
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            self.end_date = None
        assert self.start_date < self.end_date, "end_date is before start_date."
        self.location = location
        self.file_dir = file_dir
        self._load_files(n_workers)
    
    def _load_files(self, n_workers: int = 1):
        if n_workers > 1:
            self.files = p_map(lambda f: parse_weatherfile(filepath = f, location = self.location), self._filelist(), num_cpus=n_workers)
        else:
            self.files = [parse_weatherfile(filepath = file, location = self.location) for file in tqdm(self._filelist())]

    def __str__(self) -> str:
        if self.start_date and not self.end_date:
            return f"WeatherFileStack for {self.location} from {self.start_date}"
        elif self.end_date and not self.start_date:
            return f"WeatherFileStack for {self.location} to {self.end_date}"
        elif self.start_date and self.end_date:
            return f"WeatherFileStack for {self.location} from {self.start_date} to {self.end_date}"
        
    def _repr_pretty_(self, p, cycle) -> str:
        return p.text(str(self) if not cycle else '...')

    def _filelist(self):
        if (not self.start_date) and (not self.end_date):
            globlist = [glob(os.path.join(self.file_dir, f"*_{self.location}.json"))]
        else:
            if self.start_date and self.end_date:
                start = self.start_date
                end = self.end_date
            elif self.start_date:
                start = self.start_date
                end = datetime.now().date()
            elif self.end_date:
                start = datetime.strptime(os.path.basename(sorted(glob(os.path.join(self.file_dir, f"*_{self.location}.json")))[0])[:8], "%Y%m%d").date()
                end = self.end_date
            globlist = [glob(os.path.join(self.file_dir, f"{d.strftime('%Y%m%d')}*_{self.location}.json")) for d in _daterange(start, end)]
        
        if len(globlist) > 0:
            return sorted([l for dl in globlist for l in dl])
        else:
            raise ValueError(f"No WeatherFiles found for location '{self.location}' in the given time range.")
