import random
import logging
import json
import time
import datetime
import math
from urllib.parse import urlparse
from typing import List, Optional
from bs4 import BeautifulSoup as Soup
from requests_cache import CachedSession
from tqdm import tqdm

from database import ChromeHistoryDatabase

_logger = logging.getLogger(__name__)


class Theme:
    def __init__(self, from_string: str, cache: CachedSession):
        self.cached_request = cache
        # load the list of urls from a config file with tons of websites that could be visited,
        # generated from ChatGPT and various other bright minds on the internet.
        _logger.info(f"Using {from_string} theme!")
        with open("data/themes.json") as json_config:
            self.config = json.loads(json_config.read())[from_string]  # todo: theme could be invalid, maybe check...

    def get_single_website(self) -> str:
        """return a single website from the config"""
        # todo: needs to return the title like below function
        return random.choice(self.config['single_visit'])

    def get_simulation_urls(self, throttle: float = 0.01,
                            with_soup: bool = False, maximum: int = 6) -> List[List[Optional[str]]]:
        if not with_soup:
            return random.choice(self.config['sessions'])
        else:  # actually visit the urls (ie: run a simulation)
            simulation = random.choice(self.config['click_random_links'])
            _logger.debug(f"Running simulation for {simulation}")
            page_html = Soup(self.cached_request.get(simulation['url']).content, 'html.parser')
            all_urls = page_html.select(simulation['selector'])
            if len(all_urls) < 1:
                _logger.warning(f"Soup did not find any links on {simulation['url']} with {simulation['selector']}")

            random.shuffle(all_urls)
            urls = []
            for i in tqdm(range(min(len(all_urls), maximum))):
                url = all_urls[i].attrs[simulation['attr']]
                if urlparse(simulation['url']).hostname not in url:  # todo: needs one liner to impress people
                    url = urlparse(simulation['url']).scheme + "://" + urlparse(simulation['url']).hostname + url

                try:
                    title = Soup(self.cached_request.get(url).content, 'html.parser').find('title').string
                except AttributeError:
                    _logger.debug(f"Problem getting page title for {url}")
                    title = urlparse(simulation['url']).hostname  # a fallback

                urls.append([url, title])
                time.sleep(throttle)  # todo: only throttle if not cached ?

            return urls


class ThemedSpoofer:
    def __init__(self, database: ChromeHistoryDatabase, days_ago: int, daily_visits: int, avg_range: int,
                 daily_sessions: int, theme: str = "default", cache: bool = True):
        self.database = database
        self.days_to_time_travel = days_ago
        self.daily_visits = daily_visits  # how many websites are visited every day +- avg_range
        self.daily_sessions = daily_sessions  # how many browsing sessions a day (ie: breakfast, bedtime)
        self.avg_range = avg_range
        # todo: i don't know if setting cache to expire_after 1 "disables" it for the run...
        self.cached_request = CachedSession('spoof_cache', use_temp=True, expire_after=-1 if cache else 1)
        self.theme = Theme(from_string=theme, cache=self.cached_request)

    def reset_cache(self):
        self.cached_request.cache.clear()
        pass

    def generate_history(self, throttle_time: float):
        for days_ago in range(self.days_to_time_travel):
            for session in range(self.daily_sessions):
                # todo: spice this up a bit, and build out other functions / randomness
                # todo: include the random range threshold in calculation
                visits = math.floor(self.daily_visits / self.daily_sessions)
                web_visits = self.theme.get_simulation_urls(with_soup=True, maximum=visits, throttle=throttle_time)
                for visit in web_visits:
                    d = datetime.timedelta(days=days_ago)  # todo: this needs to be a date ?
                    #self.database.insert_web_visit(visit[0], visit[1], date=d)
                    print(visit[0])
