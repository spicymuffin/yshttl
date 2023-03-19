import requests
import os
import threading
import time
import datetime

WORKING_DIR = os.getcwd()
CONFIG_FILE_NAME = "config.txt"
CONFIG_FILE_PATH = WORKING_DIR + '\\' + CONFIG_FILE_NAME
LOCAL_LIST_REFRESH_TIME = 20  # in seconds


BOOK_QUEUE = []

# create empty config file if it doesnt exist
if not os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'w') as file:
        pass

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
    def __init__(self, _origin, _departure_datetime, _seats_available, _handle):
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


class DestinationArgFormatError():
    pass

class TimeArgFormatError():
    pass

class DateArgFormatError():
    pass

# route origin (si/so) date max allowed dep time
# arg format: xx mmdd h:m
def book_handler(args):
    try:
        y = -1
        m = -1
        d = -1
        h = -1
        m = -1
        # parse args
        if args[1] == "si" or "so":
            origin = args[1]
        else:
            raise DestinationArgFormatError

        try:
            m = args[2][0:2]
            d = args[2][2:4]
        except:
            raise DateArgFormatError

        try:
            splt = args[3].split(":")
            t = splt[0]
            m = splt[1]
        except:
            raise TimeArgFormatError

        # construct route object

        td = datetime.date.today()
        if td.month < m:
            y = td.year + 1
        else:
            y = td.year
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
        else:
            cprint(f"{cmd} is not recognized as a command")


def local_update():
    while True:
        time.sleep(LOCAL_LIST_REFRESH_TIME)
        # pull data from website, put into a list of Route objects


console_handler()

# requests code
# r = requests.get()
