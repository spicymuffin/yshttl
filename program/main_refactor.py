from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from urllib.request import urlopen
import os
import threading
import time
import datetime
import auth_master
import server_interface
import json
from rich.console import Console
import rich
from rich import print as rprint
from pprint import pprint

# region file management
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME
# endregion

USERID = "**replaced USERID using filter-repo**"
USERPW = "**replaced PW using filter-repo**"
WMONID = ""
JSESSIONID = ""
CLOCK_REFRESH_RATE = 1/4  # in seconds
BOOK_TIME = datetime.time(13, 55, 0)

CONSOLE = None
SCHEDULE = None


# region utility functions
def datetime_to_str_date(_datetime):
    """parse out date from datetime object and format it to yyyymmdd

    Args:
        _datetime (datetime): datetime to parse out the date from

    Returns:
        str: formatted date
    """
    return str(_datetime.year) + format(_datetime.month, "0>2") + format(_datetime.day, "0>2")


def datetime_to_str_time(_datetime):
    """parse out time from datetime object and format it to hhmm

    Args:
        _datetime (datetime): datetime to parse out the time from

    Returns:
        str: formatted time
    """
    return format(_datetime.hour, "0>2") + format(_datetime.minute, "0>2")
# endregion

# region console i/o


def cprint(msg, main=True):
    s = str(msg)
    s = s.replace('\n', '\n    ')
    if main:
        print(">>> " + s)
    else:
        print("\n>>> " + s, flush=True)
        print("<<< ", end="", flush=True)


def cinput(indent=False):
    if not indent:
        return input("<<< ")
    else:
        return input("    <<< ")
# endregion

# region classes


class WishlistRoute:
    """represent wishlisted routes
    """

    def __init__(self, _origin="S", _departure_datetime=datetime.datetime.now()) -> None:
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.str_departure_date = datetime_to_str_date(_departure_datetime)
        self.str_departure_time = datetime_to_str_time(_departure_datetime)

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=1) -> str:
        if verbose:
            return f"""date: {self.departure_datetime.date()} time: {self.departure_datetime.time()} origin: {self.origin}"""
        else:
            return str(self.departure_datetime.time())


class Route:
    """represent existing routes
    """

    def __init__(self, _origin="S", _departure_datetime=datetime.datetime.now(), _seats_available=-1) -> None:
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.seats_available = _seats_available
        self.str_departure_date = datetime_to_str_date(_departure_datetime)
        self.str_departure_time = datetime_to_str_time(_departure_datetime)

    def import_dictionary(self, _dct):
        self.dct = _dct
        self.origin = _dct["areaDivCd"]
        year = int(_dct["stdrDt"][0:4])
        month = int(_dct["stdrDt"][4:6])
        day = int(_dct["stdrDt"][6:8])
        hour = int(_dct["beginTm"][0:2])
        minute = int(_dct["beginTm"][2:4])
        self.departure_datetime = datetime.datetime(
            year, month, day, hour, minute)
        self.seats_available = int(_dct["remndSeat"])

    def book(self):
        server_interface.book_shttl(self.dct)

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=0) -> str:
        if verbose:
            return f"""date: {self.departure_datetime.date()} time: {self.departure_datetime.time()} origin: {self.origin} remdSt: {self.seats_available}"""
        else:
            return str(self.departure_datetime.time())

# endregion classes


def check_auth_and_exec(func, args):
    if not server_interface.check_login():
        cookies = auth_master.get_auth_cookies(USERID, USERPW)
        if isinstance(cookies, Exception):
            cprint(f"failed to authenticate: {cookies}")
            return check_auth_and_exec(func, args)
        with open(COOKIE_JAR_FILE_PATH, 'w') as file:
            file.write(cookies[0] + '\n' + cookies[1])
        WMONID = cookies[0]
        JSESSIONID = cookies[1]
        server_interface.WMONID = WMONID
        server_interface.JSESSIONID = JSESSIONID

    return func(*args)


def get_shttl_map(_date):
    """get shttl map on date _date

    Args:
        _date (str): date in yyyymmdd format

    Returns:
        int: -1 on failure, 0 on success
    """
    global WMONID
    global JSESSIONID

    temp_lst_S = server_interface.get_shttl_list('S', _date)
    temp_lst_I = server_interface.get_shttl_list('I', _date)

    shttl_map = {'date': _date, "S": [], 'I': []}

    for i in range(len(temp_lst_S)):
        rt = Route()
        rt.import_dictionary(temp_lst_S[i])
        shttl_map['S'].append(rt)

    for i in range(len(temp_lst_I)):
        rt = Route()
        rt.import_dictionary(temp_lst_I[i])
        shttl_map['I'].append(rt)

    return shttl_map


def get_shttl_map_n_days(_now, n=3):
    days = []
    for i in range(n):
        d = _now + datetime.timedelta(days=i)
        days.append(datetime_to_str_date(d))

    maps = []
    for i in range(n):
        maps.append(get_shttl_map(days[i]))

    return maps


def clock_upd():
    try:
        global NOW
        global DAYS_FROM_START
        currd = NOW.day
        while True:
            time.sleep(CLOCK_REFRESH_RATE)
            NOW = datetime.datetime.now()

            # force update when 1:55pm happens bc we want to be sneaky and close to 2 pm
            if not flag and NOW.hour >= BOOK_TIME.hour \
                    and NOW.minute >= BOOK_TIME.minute \
                    and NOW.second >= BOOK_TIME.second:
                rprint("BOOK_TIME")
                # # update next three days
                # check_auth_and_exec(update_n3d, (NOW, ))
                # # check book_queue
                # check_auth_and_exec(check_book_queue, (NOW, ))
                # cprint("forced usl, checked bookings", main=False)
                flag = True
            if currd < NOW.day:
                flag = False
                currd = NOW.day
                book_schedule_from_sd(DAYS_FROM_START)
                DAYS_FROM_START += 1
    except Exception as ex:
        cprint(f"CRASH! clock_upd_thread dead: {ex}", main=False)


def gen_shttl_map_table(_shttl_map):
    table = Table(title=_shttl_map['date'])

    table.add_column("R. No.", style="cyan", no_wrap=True)
    table.add_column("Origin", style="green")
    table.add_column("Time", style="magenta")

    table.add_column("Origin", style="green")
    table.add_column("Time", style="magenta")

    for i in range(max(len(_shttl_map['S']), len(_shttl_map['I']))):
        table.add_row(str(i),
                      'Sinchon' if i < len(_shttl_map['S']) else '-', str(_shttl_map['S'][i].departure_datetime.time()) if i < len(
            _shttl_map['S']) else '-', 'International' if i < len(_shttl_map['I']) else '-', str(_shttl_map['I'][i].departure_datetime.time()) if i < len(_shttl_map['I']) else '-')

    return table


def gen_shttl_map_panels(_shttl_map):
    S = []
    I = []
    for i in range(len(_shttl_map['S'])):
        S.append(Panel(
            f"[b]#{i}[/b][yellow] {str(_shttl_map['S'][i].departure_datetime.time())}", expand=True, title_align="right"))

    for i in range(len(_shttl_map['S'])):
        I.append(Panel(
            f"[b]#{i}[/b][yellow] {str(_shttl_map['I'][i].departure_datetime.time())}", expand=True, subtitle_align="right"))

    return (Columns(S), Columns(I))


def startup():
    global CONSOLE
    global SCHEDULE

    # region load cookies and config
    with open(CONFIG_FILE_PATH, 'r') as file:
        SCHEDULE = json.load(file)

    if os.path.exists(COOKIE_JAR_FILE_PATH):
        with open(COOKIE_JAR_FILE_PATH, 'r') as file:
            WMONID = file.readline()[:-1]  # dont include \n
            JSESSIONID = file.readline()

    server_interface.WMONID = WMONID
    server_interface.JSESSIONID = JSESSIONID
    # endregion

    # check cookie validity
    if not server_interface.check_login():
        cookies = auth_master.get_auth_cookies(USERID, USERPW)
        if isinstance(cookies, Exception):
            cprint(f"failed to authenticate on startup: {cookies}")
            return
        with open(COOKIE_JAR_FILE_PATH, 'w') as file:
            file.write(cookies[0] + '\n' + cookies[1])
        WMONID = cookies[0]
        JSESSIONID = cookies[1]
        server_interface.WMONID = WMONID
        server_interface.JSESSIONID = JSESSIONID

    # init console
    CONSOLE = Console()
    CONSOLE.print("Hello", "World!", style="bold red")

    maps = get_shttl_map_n_days(datetime.datetime.now(), 4)
    CONSOLE.print(maps)

    t = gen_shttl_map_table(maps[1])
    CONSOLE.print(t)


startup()
