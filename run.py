import json
from weathercrawler import WeatherCrawler


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    crawler = WeatherCrawler(**config)

    crawler.crawl()