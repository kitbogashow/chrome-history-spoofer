import os
from datetime import datetime
import random as rn
import argparse
import platform
import sqlite3
import tqdm
from typing import List


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
    parser.add_argument('path', nargs='?', default=None)
    args = parser.parse_args()

    dbpath = args.path if args.path else get_default_history_path()

    if not os.path.exists(dbpath):
        raise LookupError(f"Unale to find chrome database automatically... try using >>>spoof.py <path>")

    con = sqlite3.connect(dbpath)
    cur = con.cursor()

    then = datetime(1601, 1, 1)
    today = datetime.now()
    epoc = int((today - then).total_seconds() * 1000000)

    query = f"""INSERT INTO urls (url, title, visit_count,  last_visit_time, hidden) VALUES('https://kitboga.com', 
                                'kitboga', 1, {epoc}, 0) """

    try:
        cur.execute(query)
        con.commit()
    except sqlite3.OperationalError:
        raise PermissionError('Chrome should not be running...')

    lid = cur.lastrowid
    dur = rn.randint(999, 999999)
    query2 = f"""INSERT INTO visits (url, visit_time, visit_duration, from_visit, transition, segment_id) VALUES 
                                    ({lid}, {epoc}, {dur}, 0, 805306376, 0) """
    try:
        cur.execute(query2)
        con.commit()
    except sqlite3.OperationalError as err:
        print(err)
    except Exception as err:
        print(err)
    cur.close()

    if cur.lastrowid:
        print('record inserted!')

    con.close()
