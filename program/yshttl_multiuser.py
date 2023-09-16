# custom
import table_gen
import server_interface
import auth_master

# pip
import threading
import datetime
import json
import time
import os

# rich
from rich.console import Console

# region constants
# region file management
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_FILE_NAME = "schedule_multiuser.json"
SCHEDULE_FILE_PATH = CURR_PATH + "\\" + SCHEDULE_FILE_NAME
CONFIG_FILE_NAME = "config_multiuser.json"
CONFIG_FILE_PATH = CURR_PATH + "\\" + CONFIG_FILE_NAME
# endregion


# region config file defined
# region users
USERS = []
DEFAULT_USER = None
ACTIVE_USER = DEFAULT_USER
# endregion

# region refresh rates
REFRESH_RATE_CLOCK = 1 / 4  # in seconds
REFRESH_RATE_SHTTL_LST = 30  # in seconds
# endregion

# region time related
BOOK_TIME = datetime.time(0, 2, 0)  # time of the day when bulk booking happens
DAYS_FROM_START = 7  # fill buffer length (in days)
AUTH_SESSION_LENGTH = 60 * 5  # in seconds
# endregion

# region bools
DEBUG = False  # enable debuggin mode
CLEAN_SCHEDULE = False  # set clean schedule for debugging purposes
IGNORE_3DAYS = True
# endregion
# endregion


# region runtime calculated
START_DAY = None
CONSOLE = None

SHTTL_MPS = []

thread_clock_upd = None

UPDATING_LOCK = False
# endregion

# region actual constants
DEFAULT_SCHEDULE = {
    "USER_00": {
        "0": [],
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
    }
}

EMPTY_SCHEDULE = {
    "0": [],
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
}

DEFAULT_CONFIG = {
    "USER_00": {
        **replaced ID using filter-repo**,
        **replaced PW using filter-repo**)

    # endregion

    # set dates, times
    NOW = datetime.datetime.now()
    START_DAY = NOW.date()

    # check auth
    check_auth_reauth()

    # startup SHTTL_LST
    update_SHTTL_LST(NOW)
    # startup SHTTL_MPS
    SHTTL_MPS = get_shttl_map_n_days(NOW)

    # book 7 days ahead
    for i in range(3 if IGNORE_3DAYS else 0, DAYS_FROM_START):
        insert_schedule_bookings(i)

    # start clock thread
    thread_clock_upd = threading.Thread(target=clock_upd)
    thread_clock_upd.daemon = True
    thread_clock_upd.start()

    # start console
    console_handler()


startup()
