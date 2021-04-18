import requests
import json
import os
from datetime import datetime


def now():
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')


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
                tstamp = datetime.strptime(t['current_condition'][0]['localObsDateTime'], '%Y-%m-%d %I:%M %p')
                tstamp_str = tstamp.strftime('%Y%m%d-%H%M')
                filename = f'{tstamp_str}_{loc}.json'
                filepath = os.path.join(self.weatherfiledir, filename)
            
                with open(filepath, "w") as f:
                    json.dump(t, f, indent=2)
                with open(self.logfilepath, "a") as f:
                    f.write(f"+ {now()}: successfully saved {filename}.\n")
                    
            except Exception as e:
                with open(self.logfilepath, "a") as f:
                    f.write(f"! {now()} Location '{loc}': SAVE_ERROR: {e}\n")
                continue
