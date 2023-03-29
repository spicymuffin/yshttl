import requests
import os
import threading
import time
import datetime
from auth_master import get_auth_cookies


CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.txt"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME
LOCAL_LIST_REFRESH_TIME = 20  # in seconds
USERID = "**replaced USERID using filter-repo**"
USERPW = "**replaced PW using filter-repo**"

WMONID = ""
JSESSIONID = ""

BOOK_QUEUE = []


with open(CONFIG_FILE_PATH, 'w') as file:
    pass

if os.path.exists(COOKIE_JAR_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as file:
        WMONID = file.readline()
        JSESSIONID = file.readline()


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


class Route:
    def __init__(self, _origin, _departure_datetime, _seats_available=-1, _handle=-1):
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.seats_available = _seats_available
        self.handle = _handle


def cprint(msg):
    print(">>> " + str(msg))


def cinput(indent=False):
    if not indent:
        return input("<<< ")
    else:
        return input("    <<< ")

# route origin (si/so) date max allowed dep time
# arg format: xx mmdd h:m
# ex:
# book si 140623 24:00


def getcookies_handler():
    cookies = get_auth_cookies(USERID, USERPW)
    with open(COOKIE_JAR_FILE_PATH, 'w') as file:
        file.write(cookies[0] + '\n' + cookies[1])
    WMONID = cookies[0]
    JSESSIONID = cookies[1]
    cprint(f"Cookies updated and stored: {cookies}")


def book_handler(args):
    args_processed = book_error_handler(args)
    if type(args_processed) == str:
        cprint(f"request couldnt be fullfilled: {args_processed}")
    else:
        r = Route(args_processed[0], args_processed[1])
        BOOK_QUEUE.append(r)
        cprint(f"route was added to wishlist successfully")


def book_error_handler(args):
    try:
        today_date = datetime.date.today()
        year = -1
        month = -1
        day = -1
        hour = -1
        minute = -1
        origin = "xx"

        # parse args sinchon songdo
        if args[1] == "so" or "si":
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


def quit_handler():
    cprint("quit? (type 'y' to confirm)")
    r = cinput(1)
    if r == 'y':
        quit(0)


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
        # pull data from website, put into a list of Route objects


console_handler()

# requests code
# r = requests.get()
