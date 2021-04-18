import pandas as pd
import json
import datetime as dt
from flatten_dict import flatten
from glob import glob
from tqdm import tqdm
from p_tqdm import p_map


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
    try:
        res['nearest_area']['weatherUrl'] = json_file['nearest_area'][0]['weatherUrl'][0]['value']
    except:
        res['nearest_area']['weatherUrl'] = None
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
        try:
            raw = prepare_dict(json.load(f), location)
        except Exception as e:
            print(f"Failed to read {file}: {e}") 
    
    data = flatten(raw, reducer='underscore')
    
    return data


def load_all(weatherfilepath, parallel=False) -> pd.DataFrame:
    
    filelist = sorted(glob(f"{weatherfilepath}/*.json"))
    if parallel:
        dict_list = p_map(load_weatherfile, filelist)
    else:
        dict_list = [load_weatherfile(file) for file in tqdm(filelist)]
    
    df = pd.DataFrame.from_dict(dict_list)
    #df.index = df['current_condition_localObsDateTime']
    df["current_condition_localObsDateTime"].apply(lambda t: dt.datetime.strptime(t, "%Y-%m-%d %I:%M %p"))
    
    return df