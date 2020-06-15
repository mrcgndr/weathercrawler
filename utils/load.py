import pandas as pd
import json
from flatten_dict import flatten
from glob import glob


def prepare_dict(json_file, location) -> dict:
    res = dict()
    res['location'] = location
    res['current_condition'] = json_file['current_condition'][0]
    res['current_condition']['weatherDesc'] = json_file['current_condition'][0]['weatherDesc'][0]['value']
    res['current_condition']['weatherIconUrl'] = json_file['current_condition'][0]['weatherIconUrl'][0]['value']
    res['nearest_area'] = json_file['nearest_area'][0]
    res['nearest_area']['areaName'] = json_file['nearest_area'][0]['areaName'][0]['value']
    res['nearest_area']['country'] = json_file['nearest_area'][0]['country'][0]['value']
    res['nearest_area']['region'] = json_file['nearest_area'][0]['region'][0]['value']
    res['nearest_area']['weatherUrl'] = json_file['nearest_area'][0]['weatherUrl'][0]['value']
    res['request'] = json_file['request'][0]
    for i, weather in enumerate(json_file['weather']):
        res[f"weather{i}"] = weather
        res[f"weather{i}"]['astronomy'] = json_file['weather'][i]['astronomy'][0]
        for j, hourly in enumerate(weather['hourly']):
            hourly['weatherDesc'] = hourly['weatherDesc'][0]['value']
            hourly['weatherIconUrl'] = hourly['weatherIconUrl'][0]['value']
            time = int(hourly['time'])
            res[f"weather{i}"][f"hourly{time:04d}"] = hourly
        res[f"weather{i}"].pop('hourly')
    
    return res


def load_weatherfile(file) -> dict:

    location = file.split('_')[1].split('.')[0] 
    with open(file, "r") as f:
        raw = prepare_dict(json.load(f), location)
    
    data = flatten(raw, reducer='underscore')
    
    return data


def load_all(weatherfilepath) -> pd.DataFrame:
    
    filelist = sorted(glob(f"{weatherfilepath}/*.json"))
    df = pd.DataFrame.from_dict([load_weatherfile(file) for file in filelist])
    df.index = df['current_condition_localObsDateTime']
    
    return df