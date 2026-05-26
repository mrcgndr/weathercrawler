import requests
import json
import os
from datetime import datetime


def now():
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')


def _get_observation_datetime(payload):
    current = payload['current_condition'][0]

    if 'localObsDateTime' in current:
        return datetime.strptime(current['localObsDateTime'], '%Y-%m-%d %I:%M %p')

    observation_time = current.get('observation_time')
    weather = payload.get('weather', [])
    if observation_time and weather and weather[0].get('date'):
        return datetime.strptime(
            f"{weather[0]['date']} {observation_time}",
            '%Y-%m-%d %I:%M %p'
        )

    return datetime.now()


def _get_output_path(base_dir, location, timestamp):
    date_dir = os.path.join(
        base_dir,
        timestamp.strftime('%Y'),
        timestamp.strftime('%m'),
        timestamp.strftime('%d'),
    )
    os.makedirs(date_dir, exist_ok=True)

    filename = f"{timestamp.strftime('%H%M')}_{location}.json"
    return os.path.join(date_dir, filename), filename


class WeatherCrawler(object):

    def __init__(self, locations, weatherfiledir, logfilepath):
        self.locations = locations
        self.weatherfiledir = weatherfiledir
        self.logfilepath = logfilepath
        if not os.path.exists(weatherfiledir):
            os.makedirs(weatherfiledir)
        if not os.path.exists(os.path.dirname(logfilepath)):
            os.makedirs(os.path.dirname(logfilepath))


    def crawl(self):
        for loc in self.locations:
            
            try:
                t = requests.get(f'http://v2.wttr.in/{loc}?format=j1').json()
            except Exception as e:
                with open(self.logfilepath, "a") as f:
                    f.write(f"! {now()} Location '{loc}': GET_ERROR: {e}\n")
                continue
                
            try:    
                tstamp = _get_observation_datetime(t)
                filepath, filename = _get_output_path(self.weatherfiledir, loc, tstamp)
            
                with open(filepath, "w") as f:
                    json.dump(t, f, indent=2)
                with open(self.logfilepath, "a") as f:
                    f.write(f"+ {now()}: successfully saved {filename}.\n")
                    
            except Exception as e:
                with open(self.logfilepath, "a") as f:
                    f.write(f"! {now()} Location '{loc}': SAVE_ERROR: {e}\n")
                continue
