import random
import tqdm
import configparser
from datetime import datetime

from database import ChromeHistoryDatabase


class Theme:
    def __init__(self, from_string: str):
        # load the list of urls from a config file with tons of websites that could be visited,
        # generated from ChatGPT and various other bright minds on the internet.
        self.config = configparser.ConfigParser()[from_string]  # todo: this might be dumb, the theme could be invalid

    def get_website(self):
        """return a single website from the config"""
        pass  # todo: return something from the config file

    def get_simulation(self):
        """return a list of urls that simulate something like browsing an online store"""
        pass  # todo: return something like [start_url, simulation_url, end_url] do random requests to visit links on simulation page

class ThemedSpoofer:
    def __init__(self, database: ChromeHistoryDatabase, time_travel_to: datetime, theme: str = None):
        self.database = database
        self.start_date = time_travel_to
        self.theme = Theme(from_string=theme) if theme else None

    def generate_history(self, avg_daily_visits: int, daily_sessions: int):
        pass  # todo: do some math to figure out how often websites should be visited to make it seem semi real
