import os
import json
from weathercrawler import WeatherCrawler


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        config = json.load(f)

    crawler = WeatherCrawler(**config)

    crawler.crawl()
