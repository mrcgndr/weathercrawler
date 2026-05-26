import json
import os
from datetime import datetime, timedelta

import requests


def now():
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')


def _normalize_observation_datetime(observed_at, fetched_at):
    if observed_at > fetched_at:
        return observed_at - timedelta(days=1)
    return observed_at


def _get_observation_datetime_from_time(observation_time, fetched_at):
    observed_at = datetime.strptime(
        f"{fetched_at.strftime('%Y-%m-%d')} {observation_time}",
        '%Y-%m-%d %I:%M %p'
    )
    return _normalize_observation_datetime(observed_at, fetched_at)


def _get_observation_datetime(payload, fetched_at):
    current = payload['current_condition'][0]

    if 'localObsDateTime' in current:
        observed_at = datetime.strptime(current['localObsDateTime'], '%Y-%m-%d %I:%M %p')
        return _normalize_observation_datetime(observed_at, fetched_at)

    observation_time = current.get('observation_time')
    if observation_time:
        return _get_observation_datetime_from_time(observation_time, fetched_at)

    raise ValueError('Weather report timestamp is missing from API response')


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
                fetched_at = datetime.now()
                t = requests.get(f'http://v2.wttr.in/{loc}?format=j1').json()
            except Exception as e:
                with open(self.logfilepath, "a") as f:
                    f.write(f"! {now()} Location '{loc}': GET_ERROR: {e}\n")
                continue
                
            try:    
                tstamp = _get_observation_datetime(t, fetched_at)
                filepath, filename = _get_output_path(self.weatherfiledir, loc, tstamp)
            
                with open(filepath, "w") as f:
                    json.dump(t, f, indent=2)
                with open(self.logfilepath, "a") as f:
                    f.write(f"+ {now()}: successfully saved {filename}.\n")
                    
            except Exception as e:
                with open(self.logfilepath, "a") as f:
                    f.write(f"! {now()} Location '{loc}': SAVE_ERROR: {e}\n")
                continue
