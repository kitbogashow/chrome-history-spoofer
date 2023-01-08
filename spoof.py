import os
import argparse
import platform
from typing import List
from datetime import datetime
from dateutil import parser as date_parser

from database import ChromeHistoryDatabase
from themed_spoofer import ThemedSpoofer


def fetch_titles_from_search():
    pass


def get_default_history_path() -> str:
    if platform.system() == "Darwin":  # osx/mac
        cwd_path: List[str] = os.getcwd().split('/')
        return f"/{cwd_path[1]}/{cwd_path[2]}/Library/Application Support/Google/Chrome/Default/History"
    else:  # windows (won't work for other platforms right now)
        return f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"


""" spoof chrome history on mac or windows """
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Chrome History Spoofer', description='Inserts website visits into Chrome')
    parser.add_argument('-p', '--path', default=None, help="Path to Chrome's sqlite database, ")
    parser.add_argument('-d', '--start-date', default=datetime.now(), help="How far back in time to start the spoof, "
                                                                           "formatted as a date and time.")
    parser.add_argument('-a', '--avg-daily-visits', default=12, help="About how many websites are visited each day")
    parser.add_argument('-s', '--sessions', default=2, help="How many internet 'sessions' per day")
    parser.add_argument('-t', '--theme', default=None, help="If you want to select a theme: (Sports, News, Grandma)")
    args = parser.parse_args()

    dbpath = args.path if args.path else get_default_history_path()

    if not os.path.exists(dbpath):
        raise LookupError(f"Unable to find chrome database automatically... try: spoof.py -p <path>")

    history_db = ChromeHistoryDatabase(path=dbpath)

    spoofer = ThemedSpoofer(history_db, time_travel_to=date_parser.parse(args.start_time), theme=args.theme)
    spoofer.generate_history(args.avg_daily_visits, args.sessions)
