from datetime import datetime, timedelta
import random as rn
import sqlite3
import validators
import logging

_logger = logging.getLogger(__name__)


def _date_to_chrome_epoc(date):
    """chrome has a weird way of doing this so now i am forced to convert it myself thanks obama"""
    return int((date - datetime(1601, 1, 1)).total_seconds() * 1000000)


class ChromeHistoryDatabase:
    """this class is here because then the spoof.py looks cool"""

    def __init__(self, path: str):
        self.con = sqlite3.connect(path)

    def insert_web_visit(
        self,
        url: str,
        title: str,
        date: datetime = datetime.now(),
        duration: int = rn.randint(10, 3600),
    ):

        if not validators.url(url):
            raise ValueError(f"{url} is not a valid url >> {validators.url(url)}")

        cur = self.con.cursor()
        epoc = _date_to_chrome_epoc(date)

        try:
            cur.execute(f"INSERT INTO urls (url, title, visit_count, last_visit_time, hidden) VALUES (?, ?, ?, ?, ?)", (url, title, 1, epoc, 0))
            self.con.commit()
            cur.execute(f"INSERT INTO visits (url, visit_time, visit_duration, from_visit, transition, \
                        segment_id) VALUES (?, ?, ?, ?, ?, ?)", (cur.lastrowid, epoc, duration, 0, 805306376, 0))
            self.con.commit()
        except sqlite3.OperationalError as e:
            _logger.error(e)

        cur.close()
