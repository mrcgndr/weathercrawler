#!/usr/bin/env python3

import json
import os

from weathercrawler import WeatherCrawler


def main() -> None:
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        config = json.load(f)

    crawler = WeatherCrawler(**config)
    crawler.crawl()


if __name__ == '__main__':
    main()
