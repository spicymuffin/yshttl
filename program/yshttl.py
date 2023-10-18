# custom
import table_gen
import server_interface
import email_interface
import auth_master

# pip
import threading
import datetime
import json
import time
import os
import sys
import msvcrt

# rich
from rich.console import Console

# turn off warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# region main program

# region constants
# region file management
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_SUBFOLDER_NAME = "jsons"
LOGS_SUBFOLDER_NAME = "logs"
SCHEDULE_FILE_NAME = "schedule_multiuser.json"
SCHEDULE_FILE_PATH = (
    CURR_PATH + "\\" + JSON_SUBFOLDER_NAME + "\\" + SCHEDULE_FILE_NAME
)
CONFIG_FILE_NAME = "config_multiuser.json"
CONFIG_FILE_PATH = (
    CURR_PATH + "\\" + JSON_SUBFOLDER_NAME + "\\" + CONFIG_FILE_NAME
)
# endregion

# region config file defined
# region users
USERS = []
ACTIVE_USER = None

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
EMAIL_SERVER = True
RUN_MAINLOOP = True
# endregion
# endregion


# region runtime calculated
START_DAY = None
CONSOLE = None

SHTTL_MPS = []  # global shuttle maps for all users

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
    "USER_00": {**replaced ID using filter-repo**, **replaced PW using filter-repo**,
    # )
    # print(eq)
    # book_email_query_handler(eq)
