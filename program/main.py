import requests
import os
import threading
import time
import datetime
import auth_master
import server_interface

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.txt"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME
LOCAL_LIST_REFRESH_TIME = 60*5  # in seconds
USERID = "**replaced USERID using filter-repo**"
USERPW = "**replaced PW using filter-repo**"

WMONID = ""
JSESSIONID = ""

BOOK_QUEUE = []

SHTTL_LIST_S = []
SHTTL_LIST_I = []

ENABLE_CONSOLE = 1
DEBUG = 1

# region manage files
with open(CONFIG_FILE_PATH, 'w') as file:
    pass

if os.path.exists(COOKIE_JAR_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as file:
        WMONID = file.readline()
        JSESSIONID = file.readline()
# endregion

server_interface.WMONID = WMONID
server_interface.JSESSIONID = JSESSIONID

# region timetable format
# we need a system to set a schedule:
# timetable in config file:

"""
MON si dep 8:00
TUE
WED
THU
FRI so dep 10:00
SAT
SUN
"""
# use this ^ format to tell program which days it should automatically book bus
# endregion

# region console i/o


def cprint(msg):
    s = str(msg)
    s = s.replace('\n', '\n    ')
    print(">>> " + s)


def cinput(indent=False):
    if not indent:
        return input("<<< ")
    else:
        return input("    <<< ")
# endregion


class Route:
    def __init__(self, _origin="S", _departure_datetime=datetime.datetime.now(), _seats_available=-1) -> None:
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.seats_available = _seats_available
        self.str_departure_date = str(_departure_datetime.year) + format(
            _departure_datetime.month, "0>2") + format(_departure_datetime.day, "0>2")
        self.str_departure_time = format(_departure_datetime.month, "0>2")

    def import_dictionary(self, _dct):
        self.dct = _dct
        self.origin = _dct["areaDivCd"]
        year = int(_dct["stdrDt"][0:4])
        month = int(_dct["stdrDt"][5:6])
        day = int(_dct["stdrDt"][7:8])
        hour = int(_dct["beginTm"][0:2])
        minute = int(_dct["beginTm"][3:4])
        self.departure_datetime = datetime.datetime(
            year, month, day, hour, minute)
        self.seats_available = int(_dct["remndSeat"])

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"""  date: {self.departure_datetime.date()}
  time: {self.departure_datetime.time()}
origin: {self.origin}
remdSt: {self.seats_available}"""

# region commands
# region getcookies cmd


def getcookies_handler():
    global WMONID
    global JSESSIONID
    cookies = auth_master.get_auth_cookies(USERID, USERPW)
    if isinstance(cookies, Exception):
        cprint(f"failed to authenticate: {cookies}")
        return
    with open(COOKIE_JAR_FILE_PATH, 'w') as file:
        file.write(cookies[0] + '\n' + cookies[1])
    WMONID = cookies[0]
    JSESSIONID = cookies[1]
    server_interface.WMONID = WMONID
    server_interface.JSESSIONID = JSESSIONID
    cprint(f"cookies updated and stored: {cookies}")
# endregion


# region book cmd

# route origin (I/S) date max allowed dep time
# arg format: xx mmdd h:m
# ex:
# book I 140623 24:00

def insert_route_BOOK_QUEUE(_route):
    global BOOK_QUEUE
    lbq = len(BOOK_QUEUE)
    if lbq == 0:
        BOOK_QUEUE.append(_route)
    for i in range(lbq):
        if BOOK_QUEUE[i].departure_datetime <= _route.departure_datetime:
            BOOK_QUEUE.insert(_route, i+1)


def book_handler(args):
    args_processed = book_argument_parser(args)
    if type(args_processed) == str:
        cprint(f"request couldnt be fullfilled: {args_processed}")
    else:
        r = Route(args_processed[0], args_processed[1])
        insert_route_BOOK_QUEUE(r)
        cprint(f"route was added to wishlist successfully")


def book_argument_parser(args):
    try:
        today_date = datetime.date.today()
        year = -1
        month = -1
        day = -1
        hour = -1
        minute = -1
        origin = "xx"

        # parse args sinchon songdo
        if args[1] == "I" or "S":
            origin = args[1]
        else:
            return "DestinationArgFormatError"

        try:
            if len(args[2]) == 4:
                month = args[2][0:2]
                day = args[2][2:4]
                if today_date.month < month:
                    year = today_date.year + 1
                else:
                    year = today_date.year

            elif len(args[2]) == 6:
                month = args[2][0:2]
                day = args[2][2:4]
                year = int("20" + args[2][4:6])
            else:
                return "DateArgFormatError"
        except:
            return "DateArgFormatError"

        try:
            splt = args[3].split(":")
            hour = splt[0]
            minute = splt[1]
        except:
            return "TimeArgFormatError"

        try:
            date_time = datetime.datetime(int(year), int(
                month), int(day), int(hour), int(minute))
            if date_time < datetime.datetime.now():
                return "InvalidTimeError: DateTime has passed"
            else:
                return [origin, date_time]
        except Exception as ex:
            return f"InvalidTimeError: DateTime invaild {ex}"

    except Exception as ex:
        cprint(f"request couldnt be fullfilled: {ex}")
# endregion


# region quit cmd
def quit_handler():
    cprint("quit? (type 'y' to confirm)")
    r = cinput(1)
    if r == 'y':
        quit(0)
# endregion
# endregion


def update_SHTTL_LIST(_origin, _date):
    """update internal representation of available routes

    Args:
        _origin (str): route origin S or I or B for both
        _date (str): date in yyyymmdd format

    Returns:
        int: -1 on fail, 0 on success
    """
    global WMONID
    global JSESSIONID

    if not server_interface.check_login_state(WMONID, JSESSIONID):
        return -1
    if _origin == "B" or _origin == "S":
        if DEBUG:
            cprint("---------S---------")
        temp_lst = server_interface.get_shttl_list("S", _date)
        SHTTL_LIST_S.clear()
        for i in range(len(temp_lst)):
            rt = Route()
            rt.import_dictionary(temp_lst[i])
            SHTTL_LIST_S.append(rt)
        if DEBUG:
            cprint('\n-------------------\n'.join(map(str, SHTTL_LIST_S)))

    if _origin == "B" or _origin == "I":
        if DEBUG:
            cprint("---------I---------")
        temp_lst = server_interface.get_shttl_list("I", _date)
        SHTTL_LIST_I.clear()
        for i in range(len(temp_lst)):
            rt = Route()
            rt.import_dictionary(temp_lst[i])
            SHTTL_LIST_I.append(rt)
        if DEBUG:
            cprint('\n-------------------\n'.join(map(str, SHTTL_LIST_I)))

    return 0


def console_handler():
    while True:
        inp = cinput()
        inp_parsed = inp.split(" ")
        cmd = inp_parsed[0]
        if cmd == "book":
            book_handler(inp_parsed)
        elif cmd == "quit":
            quit_handler()
        elif cmd == "getcookies":
            getcookies_handler()
        else:
            cprint(f"{cmd} is not recognized as a command")


def local_update():
    while True:
        time.sleep(LOCAL_LIST_REFRESH_TIME)
        update_SHTTL_LIST()


if DEBUG:
    pass
    update_SHTTL_LIST("B", "20230331")

if ENABLE_CONSOLE:
    console_handler()

# requests code
# r = requests.get()
