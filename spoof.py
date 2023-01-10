import os
import argparse
import platform
import logging
from typing import List

from database import ChromeHistoryDatabase
from themed_spoofer import ThemedSpoofer

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)  # todo: colored logging output


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
    parser.add_argument('-d', '--days-ago', default=2,
                        help="How far back in time to start the spoof, x number of days ago...")
    parser.add_argument('-a', '--avg-daily-visits', default=15, help="About how many websites are visited each day")
    parser.add_argument('--avg-threshold', default=4, help="Plus or minus average daily visits range")
    parser.add_argument('-s', '--sessions', default=2, help="How many internet 'sessions' per day")
    parser.add_argument('-t', '--theme', default="default", help="If you want to select a theme: (Boomer, Sports)")
    parser.add_argument('--throttle', default=0.25, help="Throttle time between requests.")
    parser.add_argument('-cc', '--clear-cache', action="store_true", help="Clear the web requests cache.")
    parser.add_argument('-dc', '--disable-cache', action="store_true", help="Disable web requests caching.")
    args = parser.parse_args()

    dbpath = args.path if args.path else get_default_history_path()

    if not os.path.exists(dbpath):
        raise LookupError(f"Unable to find chrome database automatically... try: spoof.py -p <path>")

    history_db = ChromeHistoryDatabase(path=dbpath)

    # todo: consider checking if chrome is running? because otherwise it will throw errors after trying to add values

    spoofer = ThemedSpoofer(history_db, days_ago=args.days_ago, theme=args.theme,
                            cache=not args.disable_cache, daily_visits=args.avg_daily_visits,
                            avg_range=args.avg_threshold, daily_sessions=args.sessions)
    if args.clear_cache:
        spoofer.reset_cache()
    spoofer.generate_history(args.throttle)
