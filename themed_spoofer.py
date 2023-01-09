import random
import logging
import json
import requests
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup as Soup
from tqdm import tqdm

from database import ChromeHistoryDatabase

_logger = logging.getLogger(__name__)


class Theme:
    def __init__(self, from_string: str):
        # load the list of urls from a config file with tons of websites that could be visited,
        # generated from ChatGPT and various other bright minds on the internet.
        _logger.info(f"Using {from_string} theme!")
        with open("data/themes.json") as json_config:
            self.config = json.loads(json_config.read())[from_string]  # todo: theme could be invalid, maybe check...

    def get_single_website(self) -> str:
        """return a single website from the config"""
        return random.choice(self.config['single_visit'])

    def get_simulation_urls(self, with_soup: bool = False, maximum: int = 6) -> List[List[Optional[str]]]:
        if not with_soup:
            return random.choice(self.config['sessions'])
        else:  # actually visit the urls (ie: run a simulation)
            simulation = random.choice(self.config['click_random_links'])
            _logger.debug(f"Running simulation for {simulation}")
            page_html = Soup(requests.get(simulation['url']).content, 'html.parser')
            all_urls = page_html.select(simulation['selector'])
            random.shuffle(all_urls)
            urls = []
            for i in tqdm(range(min(len(all_urls), maximum))):
                url = all_urls[i].attrs[simulation['attr']]
                if urlparse(simulation['url']).hostname not in url:  # todo: needs one liner to impress people
                    url = urlparse(simulation['url']).hostname + url

                try:
                    title = Soup(requests.get(url).content, 'html.parser').find('title').string
                except AttributeError:
                    _logger.debug(f"Problem getting page title for {url}")
                    title = urlparse(simulation['url']).hostname  # a fallback

                urls.append([url, title])

            return urls


class ThemedSpoofer:
    def __init__(self, database: ChromeHistoryDatabase, time_travel_to: datetime, theme: str = None):
        self.database = database
        self.start_date = time_travel_to
        self.theme = Theme(from_string=theme) if theme else Theme(from_string="default")

    def generate_history(self, avg_daily_visits: int, daily_sessions: int):
        # todo: do some math to figure out how often websites should be visited to make it seem semi real
        web_visits = self.theme.get_simulation_urls(with_soup=True, maximum=18)
        for visit in web_visits:
            print(f"{visit[1]} >> {visit[0]}")


