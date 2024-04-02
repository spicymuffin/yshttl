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
    "USER_00": {"USERID": "", "USERPW": ""},
    "CONFIG": {
        "REFRESH_RATE_CLOCK": 0.25,
        "REFRESH_RATE_SHTTL_LST": 30,
        "BOOK_TIME": "0 2 0",
        "DAYS_FROM_START": 7,
        "EMAIL_SERVER": False,
        "RUN_MAINLOOP": True,
        "AUTH_SESSION_LENGTH": 300,
        "DEBUG": False,
        "CLEAN_SCHEDULE": False,
        "IGNORE_3DAYS": True,
    },
}

VERSION = 4.0
# endregion
# endregion


# region utility functions


def datetime_to_str_date(_datetime):
    """parse out date from datetime object and format it to yyyymmdd

    Args:
        _datetime (datetime): datetime to parse out the date from

    Returns:
        str: formatted date
    """
    return (
        str(_datetime.year)
        + format(_datetime.month, "0>2")
        + format(_datetime.day, "0>2")
    )


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
def cprint_(msg, main=True):
    """print in console

    Args:
        msg (str): message
        main (bool, optional): whether run from main thread. Defaults to True.
    """
    global CONSOLE
    global ACTIVE_USER

    s = str(msg)
    s = s.replace("\n", "\n    ")
    if main:
        CONSOLE.log("[bold red]>>> [/]" + s)
    else:
        sys.stdout.flush()
        while msvcrt.kbhit():
            msvcrt.getch()

        sys.stdout.write("\r")

        CONSOLE.log("[bold red]\n>>> [/]" + s)
        CONSOLE.log(f"\n[bold green]{ACTIVE_USER.alias}> [/]", end="")

    # Try to flush the buffer
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()


def render(obj):
    global CONSOLE
    CONSOLE.print(obj)


def clog(msg, main=True):
    """log msg

    Args:
        msg (str): message
        main (bool, optional): whether run from main thread. Defaults to True.
    """
    global CONSOLE
    global ACTIVE_USER

    s = str(msg)
    if main:
        CONSOLE.log(s)
    else:
        sys.stdout.flush()
        while msvcrt.kbhit():
            msvcrt.getch()

        sys.stdout.write("\r")

        CONSOLE.log(s)
        CONSOLE.print(f"\n[bold green]{ACTIVE_USER.alias}> [/]", end="")


def cinput(indent=False):
    """get input from user

    Args:
        indent (bool, optional): whether to indent input. Defaults to False.

    Returns:
        str: user input
    """
    global CONSOLE
    global ACTIVE_USER

    # Try to flush the buffer
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()

    if not indent:
        return CONSOLE.input(f"\n[bold green]{ACTIVE_USER.alias}> [/]")
    else:
        return CONSOLE.input(f"\n[bold green]{ACTIVE_USER.alias}> [/]")


# endregion


# region classes
class WishlistRoute:
    """represent wishlisted routes"""

    def __init__(
        self,
        _owner,
        _origin="S",
        _departure_datetime=datetime.datetime.now(),
        _mode="r",
    ) -> None:
        self.owner = _owner
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.str_departure_date = datetime_to_str_date(_departure_datetime)
        self.str_departure_time = datetime_to_str_time(_departure_datetime)
        self.mode = _mode

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=False, official=False) -> str:
        if verbose:
            return (
                f"date: {self.departure_datetime.date()} "
                f"time: {self.departure_datetime.time()} "
                f"origin: {self.origin}"
            )
        if official:
            return f"dep from {'sinchon' if self.origin == 'S' else 'international'}@{self.departure_datetime.strftime('%c')}"
        else:
            return self.departure_datetime.strftime("%c")


class Route:
    """represent existing routes"""

    def __init__(
        self,
        _owner,
        _origin="S",
        _departure_datetime=datetime.datetime.now(),
        _seats_available=-1,
    ) -> None:
        self.owner = _owner
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
            year, month, day, hour, minute
        )
        self.seats_available = int(_dct["remndSeat"])

    def book(self, _cookie_override=()):
        if _cookie_override == ():
            return server_interface.book_shttl(
                self.dct, self.owner.WMONID, self.owner.JSESSIONID
            )
        else:
            WMONID_OVERRIDE = _cookie_override[0]
            JSESSIONID_OVERRIDE = _cookie_override[1]
            return server_interface.book_shttl(
                self.dct, WMONID_OVERRIDE, JSESSIONID_OVERRIDE
            )

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=0) -> str:
        if verbose:
            return (
                f"date: {self.departure_datetime.date()} "
                f"time: {self.departure_datetime.time()} "
                f"origin: {self.origin} remdSt: {self.seats_available}"
            )
        else:
            return str(self.departure_datetime.time())


class BookedRoute:
    """represent booked routes"""

    def __init__(
        self, _owner, _origin="S", _departure_datetime=datetime.datetime.now()
    ) -> None:
        self.owner = _owner
        self.origin = _origin
        self.departure_datetime = _departure_datetime
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
            year, month, day, hour, minute
        )

    def book(self):
        return server_interface.book_shttl(
            self.dct, self.owner.WMONID, self.user.JSESSIONID
        )

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=0) -> str:
        if verbose:
            return (
                f"date: {self.departure_datetime.date()} "
                f"time: {self.departure_datetime.time()} "
                f"origin: {self.origin}"
            )
        else:
            return str(self.departure_datetime.time())


class User:
    def __init__(
        self,
        _id,
        _pw,
        _index=0,
        _alias="",
        _auth_on_init=True,
        _email_query=None,
    ):
        self.id = _id
        self.pw = _pw
        self.index = _index
        self.cookies = (
            auth_master.get_auth_cookies(self.id, self.pw)
            if _auth_on_init
            else ()
        )
        self.email_query = _email_query

        self.SCHEDULE = EMPTY_SCHEDULE

        self.SHTTL_LST = []
        self.BOOK_QUEUE_SCDL = []
        self.BOOK_QUEUE_USER = []

        self.WMONID = ""
        self.JSESSIONID = ""
        self.LAST_AUTH_TIME = datetime.datetime(1999, 1, 1, 0, 0, 0)

        self.alias = _alias
        self.info = {"name": "unknown", "dept": "unknowm"}

    def __repr__(self) -> str:
        return f"# {self.index} ({self.alias})\nid: {self.id}\npw: {self.pw}"

    def __str__(self) -> str:
        return f"# {self.index} ({self.alias})\nid: {self.id}\npw: {self.pw}"

    def auth_self(self) -> None:
        return check_auth_reauth(self, True)

    def update_SHTTL_LST(self, _now):
        update_SHTTL_LST(self, _now)

    def str_schedule(self) -> str:
        return f"# {self.index} ({self.alias})\nMON: {self.SCHEDULE['0']}\nTUE: {self.SCHEDULE['1']}\nWED: {self.SCHEDULE['2']}\nTHU: {self.SCHEDULE['3']}\nFRI: {self.SCHEDULE['4']}\nSAT: {self.SCHEDULE['5']}\nSUN: {self.SCHEDULE['6']}"


# endregion =


# region auth
def check_auth_and_exec(user, func, args, force=False, pass_user=True):
    """check authorization cookies for validity and
       execute func with arguments args

    Args:
        user (User): user to auth
        func (function): function to be executed
        args (tuple): parameters for function
        force (bool, optional): force reauthorization. Defaults to False.

    Returns:
        unknown: return value of func
    """
    global NOW

    if force or (NOW - user.LAST_AUTH_TIME).seconds > AUTH_SESSION_LENGTH:
        if force or not server_interface.check_login(
            user.WMONID, user.JSESSIONID
        ):
            cookies = auth_master.get_auth_cookies(user.id, user.pw)
            if isinstance(cookies, Exception):
                clog(f"auth_master failed to authenticate: {cookies}")
                return cookies
            if cookies == "invalid user credentials":
                clog("invalid credentials detected. check config file")
                return Exception("invalid credentials")
            user.WMONID, user.JSESSIONID = cookies
            # this is probably not needed
            # server_interface.WMONID = WMONID
            # server_interface.JSESSIONID = JSESSIONID
            user.LAST_AUTH_TIME = NOW
            clog(f"re-authenticated [bold]{user.alias}[/]", False)

    if pass_user:
        return func(user, *args)
    else:
        return func(*args)


def check_auth_reauth(user, force=False):
    """check authorization cookies for validity

    Args:
        user (User): user to reauthenticate
        force (bool, optional): force reauthorization. Defaults to False.
    """

    global NOW

    cookies = None  # declare for later return

    if force or (NOW - user.LAST_AUTH_TIME).seconds > AUTH_SESSION_LENGTH:
        if force or not server_interface.check_login(
            user.WMONID, user.JSESSIONID
        ):
            cookies = auth_master.get_auth_cookies(user.id, user.pw)
            if isinstance(cookies, Exception):
                clog(f"auth_master failed to authenticate: {cookies}")
                return cookies
            if cookies == "invalid user credentials":
                clog("invalid credentials detected. check config file")
                return Exception("invalid credentials")

            user.WMONID, user.JSESSIONID = cookies

            # this is probably not needed
            # server_interface.WMONID = WMONID
            # server_interface.JSESSIONID = JSESSIONID

            user.LAST_AUTH_TIME = NOW
            clog(f"re-authenticated [bold]{user.alias}[/]", False)

    return cookies  # user's cookies


def check_credentials(user) -> bool:
    cookies = auth_master.get_auth_cookies(user.id, user.pw)
    if isinstance(cookies, Exception):
        return False
    elif cookies == "invalid user credentials":
        return False
    else:
        return True


# endregion


# region user info


def get_user_info(user):
    check_auth_reauth(user)
    raw_info = server_interface.get_user_info(user.WMONID, user.JSESSIONID)
    # remove the junk
    info = {
        "name": raw_info["gdmViewSession"]["userNm"],
        "dept": raw_info["gdmViewSession"]["deptNm"],
    }


# endregion


# region shttl_map_management
def get_shttl_map(user, _date):
    """get shttl map on date _date

    Args:
        user (User): user to get a shuttle map from
        _date (str): date in yyyymmdd format

    Returns:
        dict: shttl_map
    """

    check_auth_reauth(user)

    temp_lst_S = server_interface.get_shttl_list(
        "S", _date, user.WMONID, user.JSESSIONID
    )
    temp_lst_I = server_interface.get_shttl_list(
        "I", _date, user.WMONID, user.JSESSIONID
    )

    while temp_lst_S == -1 or temp_lst_I == -1:
        clog("get_shttl_lst failed. retrying")
        check_auth_reauth(user, force=True)
        temp_lst_S = server_interface.get_shttl_list(
            "S", _date, user.WMONID, user.JSESSIONID
        )
        temp_lst_I = server_interface.get_shttl_list(
            "I", _date, user.WMONID, user.JSESSIONID
        )

    shttl_map = {"date": _date, "S": [], "I": []}

    for i in range(len(temp_lst_S)):
        rt = Route(user)
        rt.import_dictionary(temp_lst_S[i])
        # rprint(rt.dct)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        shttl_map["S"].append(rt)

    for i in range(len(temp_lst_I)):
        rt = Route(user)
        rt.import_dictionary(temp_lst_I[i])
        shttl_map["I"].append(rt)

    return shttl_map


def get_shttl_map_n_days(user, _now, n=3):
    """get a list of shttl_maps n days from _now

    Args:
        user (User): user to get shuttle maps from
        _now (datetime): time from which the shttl_maps should be received
        n (int, optional): # of days to get. Defaults to 3.

    Returns:
        list: list of shttl_maps
    """
    days = []
    for i in range(n):
        d = _now + datetime.timedelta(days=i)
        days.append(datetime_to_str_date(d))

    maps = []
    for i in range(n):
        maps.append(get_shttl_map(user, days[i]))

    return maps


def update_SHTTL_LST(user, _now):
    """update SHTTL_LST of user assuming that only the next three days are available"""
    user.SHTTL_LST = get_shttl_map_n_days(user, _now, 3)


# endregion


# region route insertion
def insert_route_BOOK_QUEUE_SCDL(user, _route):
    """insert a schedule booking request into BOOK_QUEUE_SCDL (sorted)

    Args:
        user (User): WislistRoute insertion target
        _route (WislistRoute): route object that needs to be inserted
    """
    inserted = False
    for i in range(len(user.BOOK_QUEUE_SCDL)):
        if (
            user.BOOK_QUEUE_SCDL[i].departure_datetime
            >= _route.departure_datetime
        ):
            user.BOOK_QUEUE_SCDL.insert(i, _route)
            inserted = True
            return
    if not inserted:
        user.BOOK_QUEUE_SCDL.append(_route)


def insert_route_BOOK_QUEUE_USER(user, _route):
    """insert a schedule booking request into BOOK_QUEUE_USER (sorted)

    Args:
        user (User): WislistRoute insertion target
        _route (WislistRoute): route object that needs to be inserted
    """
    inserted = False
    for i in range(len(user.BOOK_QUEUE_USER)):
        if (
            user.BOOK_QUEUE_USER[i].departure_datetime
            >= _route.departure_datetime
        ):
            user.BOOK_QUEUE_USER.insert(i, _route)
            inserted = True
            return
    if not inserted:
        user.BOOK_QUEUE_USER.append(_route)


def insert_schedule_bookings(user, delta):
    """insert a schedule booking request into BOOK_QUEUE_SCDL on delta days
       from start of program

    Args:
        user (User): WislistRoute scan target
        delta (int): # of days from start of the program
    """
    global START_DAY
    d = START_DAY + datetime.timedelta(days=delta)
    dow_i = d.weekday()  # day of week index
    rts = user.SCHEDULE[str(dow_i)]
    for j in rts:
        splt = j["time"].split(":")
        hours = int(splt[0])
        minutes = int(splt[1])
        rdt = datetime.datetime(d.year, d.month, d.day, hours, minutes)
        if rdt - datetime.timedelta(seconds=5) > NOW:
            wrt = WishlistRoute(user, j["origin"], rdt, j["mode"])
            insert_route_BOOK_QUEUE_SCDL(user, wrt)
            # else we assume the date has already passed so bye bye


def clear_book_queue(user, _book_queue):
    if _book_queue == "SCDL":
        _book_queue = user.BOOK_QUEUE_SCDL
    elif _book_queue == "USER":
        _book_queue = user.BOOK_QUEUE_USER
    else:
        clog(
            "critical internal error. please report this bug (book_avialable func)"
        )
        exit()

    _book_queue.clear()


# endregion


# region booking funcs
def book_available(user, _book_queue, _now, main=False, n=3):
    global UPDATING_LOCK

    if _book_queue == "SCDL":
        _book_queue = user.BOOK_QUEUE_SCDL
    elif _book_queue == "USER":
        _book_queue = user.BOOK_QUEUE_USER
    else:
        clog(
            "critical internal error. please report this bug (book_avialable func)"
        )
        exit()

    if len(_book_queue) == 0:
        return

    while (
        _book_queue[0].departure_datetime + datetime.timedelta(seconds=5) < NOW
    ):
        _book_queue.pop(0)
        clog("removed expired book request", main)

    while UPDATING_LOCK:
        pass

    days = []
    for i in range(n):
        d = _now + datetime.timedelta(days=i)
        days.append(datetime_to_str_date(d))

    lst = days

    rt = _book_queue[0]

    while rt.str_departure_date in lst:
        chosen_shttl_map = None
        for i in range(len(user.SHTTL_LST)):
            if user.SHTTL_LST[i]["date"] == rt.str_departure_date:
                chosen_shttl_map = user.SHTTL_LST[i][rt.origin]
                break

        min_diff = 24 * 60 * 60  # minutes in a day
        min_diff_index = None
        found = False

        for i in range(len(chosen_shttl_map)):
            if (
                rt.mode == "r"
            ):  # switch timestamp places so we find min dst before or after
                diff = (
                    chosen_shttl_map[i].departure_datetime.timestamp()
                    - rt.departure_datetime.timestamp()
                )
            else:
                diff = (
                    rt.departure_datetime.timestamp()
                    - chosen_shttl_map[i].departure_datetime.timestamp()
                )

            if (
                min_diff > diff
                and chosen_shttl_map[i].seats_available > 0
                and diff >= 0
            ):
                min_diff_index = i
                min_diff = diff
                found = True

        if found:
            r = check_auth_and_exec(
                user, chosen_shttl_map[min_diff_index].book, (), pass_user=False
            )
            cprint_(r)
            cprint_(
                f"successfully booked shttl {'before' if rt.mode == 'l' else 'after'} ({rt.mode.upper()}) {rt.departure_datetime.time()}:\n"
                f"  origin: {chosen_shttl_map[min_diff_index].origin}\n"
                f"    date: {chosen_shttl_map[min_diff_index].departure_datetime.date()}\n"
                f"    time: {chosen_shttl_map[min_diff_index].departure_datetime.time()}\n",
                main,
            )

            del chosen_shttl_map[min_diff_index]
        else:
            cprint_(
                f"failed to book shttl:\n"
                f"  origin: {rt.origin}\n"
                f"    date: {rt.departure_datetime.date()}\n"
                f"    time: {rt.departure_datetime.time()}\n",
                main,
            )

        _book_queue.pop(0)

        if len(_book_queue) > 0:
            rt = _book_queue[0]
        else:
            break


# endregion


# region commands

# region aliases
alias_book = ["book"]
alias_quit = ["quit"]
alias_getcookies = ["getcookies", "gc"]
alias_updshttllist = ["updateshuttlelist", "updshttllist", "usl"]
alias_book_queue = ["bookqueue", "bq"]
alias_shttl_map = ["shuttlemap", "sm", "shttlmap"]
alias_clear = ["clear"]
alias_debug = ["debug", "db"]
alias_shttl_lst = ["shuttlelist", "shttllst", "sl"]
alias_force_book = ["forcebook", "fb"]
alias_booked_shttl_list = ["bookedshuttlelist", "bsl"]
alias_help = ["help"]
alias_switch_user = ["switchuser", "su"]
alias_reload_schedules = ["reloadschedules", "rs"]
alias_user_info = ["userinfo", "ui"]
alias_show_schedule = ["showschedule", "ss"]

aliases = [
    alias_book,
    alias_quit,
    alias_getcookies,
    alias_updshttllist,
    alias_book_queue,
    alias_shttl_map,
    alias_clear,
    alias_debug,
    alias_shttl_lst,
    alias_force_book,
    alias_booked_shttl_list,
    alias_help,
    alias_switch_user,
    alias_reload_schedules,
    alias_user_info,
    alias_show_schedule,
]
# endregion


# region getcookies cmd
def getcookies_handler(args):
    global ACTIVE_USER
    with CONSOLE.status("updating lock....", spinner="clock"):
        ex = check_auth_reauth(ACTIVE_USER, force=True)
    if isinstance(ex, Exception):
        cprint_(f"request couldnt be fullfilled: {ex}")
    else:
        cprint_(f"cookies updated: {ex}")


# endregion


# region debug
def debug_handler(args):
    global USERS

    for user in USERS:
        print(user.SCHEDULE)


# endregion


# region book cmd
def book_handler(args):
    global NOW
    global ACTIVE_USER

    args_processed = book_argument_parser(args)
    if type(args_processed) == str:
        # show error message
        cprint_(f"request couldnt be fullfilled: {args_processed}")
    else:
        r = WishlistRoute(
            ACTIVE_USER, args_processed[0], args_processed[1], args_processed[2]
        )
        # insert in user book queue
        insert_route_BOOK_QUEUE_USER(ACTIVE_USER, r)
        cprint_("route was added to wishlist successfully")
        # book whatever is possible in user book queue
        check_auth_and_exec(
            ACTIVE_USER, book_available, ("USER", NOW, True), False
        )


def book_argument_parser(args):
    try:
        today_date = datetime.date.today()
        year = -1
        month = -1
        day = -1
        hour = -1
        minute = -1
        origin = "xx"
        mode = "r"

        # parse args sinchon songdo
        if args[1] == "I" or "S":
            origin = args[1]
        else:
            return "DestinationArgFormatError"

        if len(args) >= 5:
            if args[4] == "l" or "r":
                mode = args[4]
            else:
                return "ModeArgFormatError"

        try:
            if len(args[2]) == 4:
                month = args[2][0:2]
                day = args[2][2:4]
                if today_date.month < month:
                    year = today_date.year + 1
                else:
                    year = today_date.year

            elif len(args[2]) == 8:
                year = int(args[2][0:4])
                month = args[2][4:6]
                day = args[2][6:8]
            else:
                return "DateArgFormatError"
        except Exception:
            return "DateArgFormatError"

        try:
            splt = args[3].split(":")
            hour = splt[0]
            minute = splt[1]
        except Exception:
            return "TimeArgFormatError"

        try:
            date_time = datetime.datetime(
                int(year), int(month), int(day), int(hour), int(minute)
            )
            if date_time < datetime.datetime.now():
                return "InvalidDateTimeError: DateTime has passed"
            else:
                return [origin, date_time, mode]
        except Exception as ex:
            return f"InvalidDateTimeError: DateTime invaild {ex}"

    except Exception as ex:
        cprint_(f"request couldnt be fullfilled: {ex}")


# endregion


# region quit cmd
def quit_handler(args):
    cprint_("quit? (type 'y' to confirm)")
    r = cinput(1)
    if r == "y":
        quit(0)


# endregion


# region updshttllist cmd
def updshttllist_handler(args):
    global NOW
    global CONSOLE
    global ACTIVE_USER

    with CONSOLE.status("updating....", spinner="clock"):
        while UPDATING_LOCK:
            pass
        ex = check_auth_and_exec(ACTIVE_USER, update_SHTTL_LST, (NOW,))
    if isinstance(ex, Exception):
        cprint_(f"request couldnt be fullfilled: {ex}")
    else:
        cprint_("SHTTL_LST updated")


# endregion


# region bookqueue cmd
def book_queue_handler(args):
    global ACTIVE_USER

    table = None
    if len(args) == 1:
        table = table_gen.gen_book_queue_table(ACTIVE_USER.BOOK_QUEUE_USER)
    else:
        if args[1] == "u" or args[1] == "user":
            table = table_gen.gen_book_queue_table(ACTIVE_USER.BOOK_QUEUE_USER)
        elif args[1] == "s" or args[1] == "schedule":
            table = table_gen.gen_book_queue_table(ACTIVE_USER.BOOK_QUEUE_SCDL)
        else:
            cprint_("request couldnt be fullfilled: invalid argument")

    if table is not None:
        render(table)


# endregion


# region shttl_map cmd
def shttl_map_handler(args):
    global NOW

    table = None
    if len(args) == 1:
        table = table_gen.gen_shttl_map_table(SHTTL_MPS[0])
    else:
        try:
            table = table_gen.gen_shttl_map_table(SHTTL_MPS[int(args[1])])
        except Exception as ex:
            clog(f"request couldnt be fullfilled: {ex}")
    if table is not None:
        render(table)


# endregion


# region shttl_lst cmd
def shttl_lst_handler(args):
    global NOW
    global ACTIVE_USER

    table = None
    if len(args) == 1:
        table = table_gen.gen_shttl_lst_table(ACTIVE_USER.SHTTL_LST)
    else:
        try:
            table = table_gen.gen_shttl_lst_table_on_date(
                ACTIVE_USER.SHTTL_LST, args[1]
            )
        except Exception as ex:
            clog(f"request couldnt be fullfilled: {ex}")
    if table is not None:
        render(table)


# endregion


# region clear cmd
def clear_handler(args):
    os.system("cls")


# endregion


# region force_book cmd
def force_book_handler(args):
    global NOW
    global ACTIVE_USER
    global SHTTL_MPS
    args_processed = force_book_argument_parser(args)
    if type(args_processed) == str:
        # show error message
        cprint_(f"request couldnt be fullfilled: {args_processed}")
    else:
        s = SHTTL_MPS[args_processed[0]][args_processed[2]][args_processed[1]]
        r = check_auth_and_exec(ACTIVE_USER, s.book, ((ACTIVE_USER.WMONID, ACTIVE_USER.JSESSIONID),), pass_user=False)
        cprint_(r)


def force_book_argument_parser(args):
    try:
        shttl_map_index = None
        shttl_index = None
        origin = None

        try:
            shttl_map_index = int(args[2])
        except Exception:
            return "ShttlMapIndexArgError"

        try:
            shttl_index = int(args[3])
        except Exception:
            return "ShttlIndexArgError"

        if args[1] != "S" and args[1] != "I":
            return "OriginArgError"
        else:
            origin = args[1]

        if not (0 <= shttl_map_index < len(SHTTL_MPS)):
            return "ShttlMapIndexValueError"

        if not (0 <= shttl_index < len(SHTTL_MPS[shttl_map_index][origin])):
            return "ShttlIndexValueError"

        return [shttl_map_index, shttl_index, origin]
    except Exception as ex:
        cprint_(f"request couldnt be fullfilled: {ex}")


# endregion


# region booked_shttl_list
def get_booked_shttl_map(user, _date):
    temp_lst = server_interface.get_booked_shttl_list(
        "S", _date, user.WMONID, user.JSESSIONID
    )

    temp_lst_S = []
    temp_lst_I = []

    for i in temp_lst:
        if i["areaDivCd"] == "S":
            temp_lst_S.append(i)
        if i["areaDivCd"] == "I":
            temp_lst_I.append(i)

    shttl_map = {"date": _date, "S": [], "I": []}

    for i in range(len(temp_lst_S)):
        rt = BookedRoute(user)
        rt.import_dictionary(temp_lst_S[i])
        shttl_map["S"].append(rt)

    for i in range(len(temp_lst_I)):
        rt = BookedRoute(user)
        rt.import_dictionary(temp_lst_I[i])
        shttl_map["I"].append(rt)

    return shttl_map


def booked_shttl_list_handler(args):
    global ACTIVE_USER
    global NOW
    global BOOKED_SHTTL_LST

    check_auth_reauth(ACTIVE_USER)

    n = 3
    days = []
    for i in range(n):
        d = NOW + datetime.timedelta(days=i)
        days.append(datetime_to_str_date(d))

    maps = []
    for i in range(n):
        x = get_booked_shttl_map(ACTIVE_USER, days[i])
        maps.append(x)

    BOOKED_SHTTL_LST = maps

    if len(args) == 1:
        table = table_gen.gen_booked_shttl_lst_table(BOOKED_SHTTL_LST)
    else:
        try:
            table = table_gen.gen_booked_shttl_lst_table_on_date(
                BOOKED_SHTTL_LST
            )
        except Exception as ex:
            clog(f"request couldnt be fullfilled: {ex}")
    if table is not None:
        render(table)


# endregion


# region help cmd
def help_handler(args):
    if len(args) == 1:
        cprint_(get_help_string(help_handler))
    else:
        for i in aliases:
            if args[1] in i:
                cprint_(get_help_string(str_to_cmd(args[1])))


# endregion


# region switch_user cmd
def switch_user_handler(args):
    global USERS
    global ACTIVE_USER

    if len(args) == 1:
        cprint_("no argument user to switch to provided")
        return

    success = False
    search_index = -1
    try:
        search_index = int(args[1])
    except Exception as ex:
        pass

    if search_index != -1:
        index = search_user_with_id(search_index)
        if index == -1:
            cprint_(f"user with index # {args[1]} doesn't exist")
            return
        else:
            ACTIVE_USER = USERS[index]
            success = True

    i = 0
    while i < len(USERS):
        if USERS[i].alias == args[1]:
            ACTIVE_USER = USERS[i]
            success = True
        i += 1
    if i == len(USERS) and success == False:
        cprint_(f"user with alias {args[1]} doesn't exist")
        return
    if success == True:
        cprint_(f"switched user to {ACTIVE_USER.alias} (# {ACTIVE_USER.index})")


# endregion


# region reload_schedules cmd
def reload_schedules_handler(args):
    global SCHEDULE_FILE_PATH

    global USERS
    global ACTIVE_USER

    global CLEAN_SCHEDULE
    global EMPTY_SCHEDULE

    global DAYS_FROM_START
    global IGNORE_3DAYS

    try:
        with open(SCHEDULE_FILE_PATH, "r") as file:
            SCHEDULE_CONFIG = json.load(file)
            SCHEDULES = SCHEDULE_CONFIG.keys()

            for key in SCHEDULES:
                usr_index = int(key.split("_")[1])
                index = search_user_with_id(usr_index)
                if index == -1:
                    cprint_(
                        f"schedule for # {key} was not assigned because the corresponding user wasnt loaded (check config?)"
                    )
                else:
                    USERS[index].SCHEDULE = SCHEDULE_CONFIG[key]

            cprint_(
                "schdules loaded for each user:\n"
                + "\n".join([x.str_schedule() for x in USERS])
            )

            if CLEAN_SCHEDULE:
                for usr in USERS:
                    usr.SCHEDULE = EMPTY_SCHEDULE
                cprint_(
                    "schdules overridden (CLEAN_SCHEDLE set to true)" + "\n"
                )

        print(ACTIVE_USER.BOOK_QUEUE_SCDL)
        users_exec(clear_book_queue, ("SCDL",))
        print(ACTIVE_USER.BOOK_QUEUE_SCDL)

        for usr in USERS:
            for i in range(3 if IGNORE_3DAYS else 0, DAYS_FROM_START):
                insert_schedule_bookings(usr, i)
        print(ACTIVE_USER.BOOK_QUEUE_SCDL)

    except Exception as ex:
        cprint_(f"couldnt reload schedules: {ex}")


# endregion


# region user_info cmd
def user_info_handler(args):
    global ACTIVE_USER

    user_info = get_user_info(ACTIVE_USER)
    cprint_(f"displaying user info for {ACTIVE_USER.alias}:\n{user_info}")


# endregion


# region show_schedule cmd
def show_schedule(args):
    global ACTIVE_USER

    cprint_(
        f"displaying schedule for {ACTIVE_USER.alias}:\n{ACTIVE_USER.SCEDULE}"
    )


# endregion

# endregion


# region console handling
def tr_wrapper(func, args):
    if func == book_handler or func == shttl_map_handler:
        with CONSOLE.status("updating lock....", spinner="clock"):
            while UPDATING_LOCK:
                pass
    func(args)


def str_to_cmd(s):
    """map a cmd str to a function obj

    Args:
        s (str): cmd str

    Returns:
        function: mapped function
    """
    if s in alias_book:
        return book_handler
    elif s in alias_quit:
        return quit_handler
    elif s in alias_getcookies:
        return getcookies_handler
    elif s in alias_updshttllist:
        return updshttllist_handler
    elif s in alias_book_queue:
        return book_queue_handler
    elif s in alias_shttl_map:
        return shttl_map_handler
    elif s in alias_clear:
        return clear_handler
    elif s in alias_debug:
        return debug_handler
    elif s in alias_shttl_lst:
        return shttl_lst_handler
    elif s in alias_force_book:
        return force_book_handler
    elif s in alias_booked_shttl_list:
        return booked_shttl_list_handler
    elif s in alias_help:
        return help_handler
    elif s in alias_switch_user:
        return switch_user_handler
    elif s in alias_reload_schedules:
        return reload_schedules_handler
    elif s in alias_user_info:
        return user_info_handler
    elif s in alias_show_schedule:
        return
    else:
        return None


def get_help_string(f):
    if f == book_handler:
        return f"function: request a shuttle booking by specifying an origin, date, time and booking mode\nformat: (alias) origin date(YYYYMMDD) time(HH:MM) mode('r' or 'l') \naliases: {alias_book}"
    elif f == quit_handler:
        return f"function: force shttl by specifying a shuttle map, route index and origin\nformat: (alias) shttl_map_index shttl_index origin\naliases: {alias_quit}"
    elif f == getcookies_handler:
        return f"function: force cookie update\nformat: (alias)\naliases: {alias_getcookies}"
    elif f == updshttllist_handler:
        return f"function: force shttl list update\nformat: (alias)\n aliases: {alias_updshttllist}"
    elif f == book_queue_handler:
        return f"function: display user's booking queue\nformat: (alias)\naliases: {alias_book_queue}\nformat: (alias) mode('u' for user bookings; 's' for schedule bookings)\naliases: {alias_book_queue}"
    elif f == shttl_map_handler:
        return f"function: display a shuttle map\nformat: (alias) shttl_map_index(optional, use to define which shttl map to display) shttl_index origin\naliases: {alias_shttl_map}"
    elif f == clear_handler:
        return f"function: force shttl by specifying a shuttle map, route index and origin\nformat: (alias) shttl_map_index shttl_index origin\naliases: {alias_clear}"
    elif f == debug_handler:
        return f"function: used for debugging purposes\n format: [cmd] shttl_map_index shttl_index origin\naliases: {alias_debug}"
    elif f == shttl_lst_handler:
        return f"function: prints out all available routes for this account at this time\nformat: (alias) shttl_lst_index(optional, use to define which part of the shttl_lst to display)\naliases: {alias_shttl_lst}"
    elif f == force_book_handler:
        return f"function: force book a shttl by specifying a origin, a shuttle map index and a route index\nformat: (alias) origin shttl_map_index shttl_index\naliases: {alias_force_book}"
    elif f == booked_shttl_list_handler:
        return f"function: display a user's booked shuttle list\nformat: (alias) ??\naliases: {alias_booked_shttl_list}"
    elif f == help_handler:
        return f"Yonsei shuttle bus command line tool ver. {VERSION}\ncommands available: {aliases}\ntype in format: command_name help to find out more about a particular command\nex: fb help\n...displays how to use the forcebook command which has an alias 'fb'"
    elif f == switch_user_handler:
        return f""
    elif f == reload_schedules_handler:
        return f""


def console_handler():
    while True:
        inp = cinput()
        inp_parsed = inp.split(" ")
        cmd = inp_parsed[0]
        exec = None
        r = str_to_cmd(cmd)
        if r is not None:
            exec = (r, inp_parsed)
        else:
            cprint_(f"'{cmd}' is not recognized as a command")
        if exec is not None:
            if len(exec[1]) >= 2 and (
                exec[1][1] == "help" or exec[1][1] == "h"
            ):
                cprint_(get_help_string(exec[0]))
            else:
                tr_wrapper(
                    exec[0],
                    exec[1],
                )


# endregion


# region multiuser handling


def users_exec(func, args):
    global USERS

    ret = []
    for usr in USERS:
        res = func(usr, *args)
        ret.append(res)
    return ret


def search_user_with_id(x):
    global USERS

    low = 0
    high = len(USERS) - 1
    mid = 0

    while low <= high:
        mid = (high + low) // 2

        # If x is greater, ignore left half
        if USERS[mid].index < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif USERS[mid].index > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return -1


# endregion

# endregion main program


# IM SORRY THIS NEEDS AN OOP ENCAPSULATION OR SMT BUT I AM SO LAZY AND SO
# CONSTRAINED BY TIME THIS IS AWFUL I KNOW BUT BARE WITH ME D:


# region email server

# region variables

EMAIL_SERVER_CONFIG_FILE_NAME = "config_email_server.json"
EMAIL_SERVER_CONFIG_FILE_PATH = (
    CURR_PATH
    + "\\"
    + JSON_SUBFOLDER_NAME
    + "\\"
    + EMAIL_SERVER_CONFIG_FILE_NAME
)
AUTHORIZED_EMAILS_LIST_FILE_NAME = "allowed_emails_list.json"
AUTHORIZED_EMAILS_LIST_FILE_PATH = (
    CURR_PATH
    + "\\"
    + JSON_SUBFOLDER_NAME
    + "\\"
    + AUTHORIZED_EMAILS_LIST_FILE_NAME
)

BOOK_QUERIES_PATH_LOOKUP_DICT = {}

QUERY_PREFIX = "query_"
# TODO: logs
# UNAUTHORIZED_EMAIL_LOG_FILE_NAME = "unauthorized_email_log.txt"
# UNAUTHORIZED_EMAIL_LOG_FILE_PATH = (
#     CURR_PATH + "\\" + LOGS_SUBFOLDER_NAME + "\\" + UNAUTHORIZED_EMAIL_LOG_FILE_NAME
# )


EMAIL_QUERIES = []

EMAIL_SERVER_BOOK_TIME = datetime.time(13, 55, 0)

AUTHORIZED_EMAILS_LIST = []
EMAIL_QUERIES_PROCESSED = []
EMAIL_QUERIES_UNPROCESSED = []
ADMIN_EMAIL = None

EMAIL_SERVER_MESSAGE_READ_REFRESH_RATE = 10  # in seconds
EMAIL_SERVER_MESSAGE_READ_BATCH_SIZE = 20

thread_email_server_upd = None

BOOK_QUEUE_EMAIL_SERVER = []

# user_00 is admin
DEFAULT_ALLOWED_EMAIL_LIST = {"admin@email.xxx": {"name": "admin"}}

DEFAULT_EMAIL_SERVER_CONFIG = {
    "RUNOPT": {
        "EMAIL_SERVER_BOOK_TIME": "13 55 0",
        "ADMIN_EMAIL": "admin@email.xxx",
    }
}

BOOK_QUERIES_SUBFLODER_NAME = "book_queries"
BOOK_QUERIES_SUBFLODER_PATH = CURR_PATH + "\\" + BOOK_QUERIES_SUBFLODER_NAME

# endregion


# YYYY/MM/DD HH:MM
def parse_serialized_date(_serialized_date) -> datetime.datetime:
    splt = _serialized_date.split(" ")
    assembly_date = splt[0]
    assembly_time = splt[1]

    assembly_date = assembly_date.split("-")
    assembly_time = assembly_time.split(":")

    assembly_year = assembly_date[0]
    assembly_month = assembly_date[1]
    assembly_day = assembly_date[2]

    assembly_hour = assembly_time[0]
    assembly_minute = assembly_time[1]
    assembly_second = assembly_time[2]

    return datetime.datetime(
        int(assembly_year),
        int(assembly_month),
        int(assembly_day),
        int(assembly_hour),
        int(assembly_minute),
        int(assembly_second),
    )


class EmailQuery:
    def __init__(self, _recv_datetime, _subject, _sender_info, _body) -> None:
        self.recv_datetime = _recv_datetime
        self.subject = _subject
        self.sender_name = (
            None if _sender_info == None else _sender_info["sender_name"]
        )
        self.sender_email = (
            None if _sender_info == None else _sender_info["sender_email"]
        )
        self.body = _body
        self.authorized = False
        self.elevated = False

        self.query_data = {"type": "undefined"}

        self.index = -1

        self.check_authorization()
        self.evaluate_query()

    def check_authorization(self):
        global AUTHORIZED_EMAILS_LIST

        if self.sender_email in AUTHORIZED_EMAILS_LIST:
            self.authorized = True

    def evaluate_query(self):
        global ADMIN_EMAIL

        if self.authorized == False:
            self.query_data["type"] = "unauthorized"
            return "unauthorized"

        if self.sender_email == ADMIN_EMAIL:
            self.elevated = True

        splt = self.body.split("\n")

        i = 0
        while i < len(splt):
            if splt[i] == "":
                del splt[i]
            else:
                i += 1

        if len(splt) == 0:
            # malformed if empty
            self.query_data["type"] = "invalid"
            return "invalid"

        splt[0] = splt[0].lower()

        if splt[0] == "add":
            # add user to authorized email list
            if self.elevated:
                if len(splt) != 3:
                    self.query_data["type"] = "invalid"
                    return "invalid"
                self.query_data["type"] = "add"
                self.query_data["add_email"] = splt[1]
                self.query_data["add_alias"] = splt[2]
                return "add"
            self.query_data["type"] = "forbidden"
            return "forbidden"

        elif splt[0] == "remove":
            # delete user from authorized email list
            if self.elevated:
                if len(splt) != 2:
                    self.query_data["type"] = "invalid"
                    return "invalid"
                self.query_data["type"] = "remove"
                self.query_data["remove_email"] = splt[1]
                return "remove"
            self.query_data["type"] = "forbidden"
            return "forbidden"

        elif splt[0] == "nuke":
            # delete all email queries
            if self.elevated:
                self.query_data["type"] = "nuke"
                return "nuke"
            self.query_data["type"] = "forbidden"
            return "forbidden"

        elif splt[0] == "show_authorized":
            # send list of authorized users
            if self.elevated:
                self.query_data["type"] = "show_authorized"
                return "show_authorized"
            self.query_data["type"] = "forbidden"
            return "forbidden"

        elif splt[0] == "book":
            # book code
            if len(splt) != 4:
                self.query_data["type"] = "invalid"
                return "invalid"
            self.query_data["type"] = "book"
            self.query_data["id"] = splt[1]
            self.query_data["pw"] = splt[2]
            self.query_data["book_details"] = splt[3]
            return "book"

        elif splt[0] == "show":
            # show active queries
            self.query_data["type"] = "show"
            return "show"

        elif splt[0] == "delete":
            # delete queries
            if len(splt) != 2:
                self.query_data["type"] = "invalid"
                return "invalid"
            self.query_data["type"] = "delete"
            self.query_data["remove_target"] = splt[1]
            return "delete"

        else:
            # complain
            self.query_data["type"] = "invalid"
            return "invalid"

    # removes user entry from query since it can be restored at runtime
    def serialize_query_data(self):
        if "user" in self.query_data.keys():
            del self.query_data["user"]
        return self.query_data

    def serialize(self):
        serialized = {
            "recv_datetime": self.recv_datetime.strftime("%F %T"),
            "subject": self.subject,
            "sender_name": self.sender_name,
            "sender_email": self.sender_email,
            "body": self.body,
            "authorized": self.authorized,
            "elevated": self.elevated,
            "query_data": self.serialize_query_data(),
        }

        return serialized

    def load(self, _serialized_data):
        self.recv_datetime = parse_serialized_date(
            _serialized_data["recv_datetime"]
        )
        self.subject = _serialized_data["subject"]
        self.sender_name = _serialized_data["sender_name"]
        self.sender_email = _serialized_data["sender_email"]
        self.body = _serialized_data["body"]
        self.authorized = _serialized_data["authorized"]
        self.elevated = _serialized_data["elevated"]

        self.query_data = _serialized_data["query_data"]

        if self.query_data["type"] == "book":
            id = self.query_data["id"]
            pw = self.query_data["pw"]
            self.query_data["user"] = User(
                id, pw, _auth_on_init=False, _email_query=self
            )

            # bruh
            self.query_data["book_arguments"]["origin"] = _serialized_data[
                "query_data"
            ]["book_arguments"]["origin"]
            self.query_data["book_arguments"][
                "departure_datetime"
            ] = parse_serialized_date(
                _serialized_data["query_data"]["book_arguments"][
                    "departure_datetime"
                ]
            )
            self.query_data["book_arguments"]["mode"] = _serialized_data[
                "query_data"
            ]["book_arguments"]["mode"]

    def __str__(self) -> str:
        return f"type: {self.query_data['type']}\nsubject: {self.subject}\nsender email: {self.sender_email}\nauthorized: {self.authorized}\nelevated: {self.elevated}\nquery_data:\n {json.dumps(self.query_data)}"


def insert_route_BOOK_QUEUE_EMAIL_SERVER(_route):
    inserted = False

    global BOOK_QUEUE_EMAIL_SERVER

    for i in range(len(BOOK_QUEUE_EMAIL_SERVER)):
        if (
            BOOK_QUEUE_EMAIL_SERVER[i].departure_datetime
            >= _route.departure_datetime
        ):
            BOOK_QUEUE_EMAIL_SERVER.insert(i, _route)
            inserted = True
            return
    if not inserted:
        BOOK_QUEUE_EMAIL_SERVER.append(_route)


def book_available_email_server(_now):
    global BOOK_QUEUE_EMAIL_SERVER
    global NOW

    n = 3

    # set book_queue
    book_queue = BOOK_QUEUE_EMAIL_SERVER

    # if book_queue is empty we leave
    if len(book_queue) == 0:
        return
    # if route is expired for some reason we leave...
    while (
        len(book_queue) > 0 and book_queue[0].departure_datetime + datetime.timedelta(seconds=5) < NOW
    ):
        os.remove(
            BOOK_QUERIES_SUBFLODER_PATH
            + "\\"
            + book_queue[0].owner.email_query.sender_email
            + "\\"
            + QUERY_PREFIX
            + "{:0>2}".format(int(book_queue[0].owner.email_query.index))
            + ".json"
        )
        book_queue.pop(0)
        clog(
            "emailserver: removed expired book request from BOOK_QUEUE_EMAIL_SERVER"
        )

    # find next 3 days
    days = []
    for i in range(n):
        d = _now + datetime.timedelta(days=i)
        days.append(datetime_to_str_date(d))
    lst = days

    # get first wishlist route so we can see if we need to book it
    rt = book_queue[0]

    # code below runs only if we CAN book it (not guaranteed but theoretically)
    while rt.str_departure_date in lst:
        # set user (email queries need authentication on book)
        user = rt.owner
        # needs to be authenticated on book
        user.auth_self()
        # update SHTTL_LST for our user
        user.update_SHTTL_LST(NOW)

        # idr what this does but it should be legit
        chosen_shttl_map = None
        for i in range(len(user.SHTTL_LST)):
            if user.SHTTL_LST[i]["date"] == rt.str_departure_date:
                chosen_shttl_map = user.SHTTL_LST[i][rt.origin]
                break

        min_diff = 24 * 60 * 60  # minutes in a day
        min_diff_index = None
        found = False

        for i in range(len(chosen_shttl_map)):
            if (
                rt.mode == "r"
            ):  # switch timestamp places so we find min dst before or after
                diff = (
                    chosen_shttl_map[i].departure_datetime.timestamp()
                    - rt.departure_datetime.timestamp()
                )
            else:
                diff = (
                    rt.departure_datetime.timestamp()
                    - chosen_shttl_map[i].departure_datetime.timestamp()
                )

            if (
                min_diff > diff
                and chosen_shttl_map[i].seats_available > 0
                and diff >= 0
            ):
                min_diff_index = i
                min_diff = diff
                found = True

        os.remove(
            BOOK_QUERIES_SUBFLODER_PATH
            + "\\"
            + user.email_query.sender_email
            + "\\"
            + QUERY_PREFIX
            + "{:0>2}".format(int(user.email_query.index))
            + ".json"
        )

        clog(
            f"emailserver: removed query no. {user.email_query.index} for {user.email_query.sender_email}"
        )

        if found:
            r = chosen_shttl_map[min_diff_index].book()
            clog(r)
            clog(
                f"emailserver: successfully booked shttl {'before' if rt.mode == 'l' else 'after'} ({rt.mode.upper()}) {rt.departure_datetime.time()}:\n"
                f"  origin: {chosen_shttl_map[min_diff_index].origin}\n"
                f"    date: {chosen_shttl_map[min_diff_index].departure_datetime.date()}\n"
                f"    time: {chosen_shttl_map[min_diff_index].departure_datetime.time()}\n"
            )
            email_interface.send_email(
                user.email_query.sender_email,
                f"😊 your request was fullfilled",
                f"yonsei server responce: {r}\n"
                f"successfully booked shuttle {'before' if rt.mode == 'l' else 'after'} ({rt.mode.upper()}) {rt.departure_datetime.time()}:\n"
                f"  origin: {chosen_shttl_map[min_diff_index].origin}\n"
                f"    date: {chosen_shttl_map[min_diff_index].departure_datetime.date()}\n"
                f"    time: {chosen_shttl_map[min_diff_index].departure_datetime.time()}\n"
                f"\n"
                f"<b>enjoy! <3</b>",
            )
            del chosen_shttl_map[min_diff_index]
        else:
            clog(
                f"emailserver: failed to book shttl:\n"
                f"  origin: {rt.origin}\n"
                f"    date: {rt.departure_datetime.date()}\n"
                f"    time: {rt.departure_datetime.time()}\n",
            )
            email_interface.send_email(
                user.email_query.sender_email,
                f"😰 your request was unfulfillable (probably)",
                f"failed to book shuttle from book queue. details:\n"
                f"  origin: {rt.origin}\n"
                f"    date: {rt.departure_datetime.date()}\n"
                f"    time: {rt.departure_datetime.time()}\n"
                f"\n"
                f"there probably werent any disponible shuttles at the date and time you requested.\n"
                f"if thats not the case please contact the administrator, any help in catching bugs\n"
                f"is reeeeeeeeeally appreciated 😄",
            )

        book_queue.pop(0)

        if len(book_queue) > 0:
            rt = book_queue[0]
        else:
            break


# region email query handlers


def unauthorized_email_query_handler(_query):
    global ADMIN_EMAIL
    email_interface.send_email(
        ADMIN_EMAIL,
        f"unauthorized access logged",
        f"an unauthorized request was made:\n"
        f"Date and Time: {_query.recv_datetime.strftime('%c')}\n"
        f"Sender: {_query.sender_email} ({_query.sender_name})"
        f"Subject: {_query.subject}\n"
        f"Body:\n{_query.body}",
    )
    clog("emailserver: unauthorized email handled")


def add_email_query_handler(_query):
    global AUTHORIZED_EMAILS_LIST_FILE_PATH
    global AUTHORIZED_EMAILS_LIST

    global ADMIN_EMAIL

    add_email = _query.query_data["add_email"]
    add_alias = _query.query_data["add_alias"]

    AUTHORIZED_EMAILS_LIST[add_email] = {"alias": add_alias}

    file = open(AUTHORIZED_EMAILS_LIST_FILE_PATH, "w")
    json.dump(AUTHORIZED_EMAILS_LIST, file)
    file.close()

    dirs = os.listdir(BOOK_QUERIES_SUBFLODER_PATH)

    for email in AUTHORIZED_EMAILS_LIST.keys():
        path = BOOK_QUERIES_SUBFLODER_PATH + "\\" + email
        if email not in dirs:
            os.mkdir(path)
            clog(
                f"emailserver: created book queries storage directory for {email}"
            )
        BOOK_QUERIES_PATH_LOOKUP_DICT[email] = path
        clog(f"emailserver: added email to BOOK_QUERIES_PATH_LOOKUP_DICT")

    email_interface.send_email(
        ADMIN_EMAIL,
        f"successful admin cmd execution notice",
        f"authorized {add_email} ({add_alias})\n",
    )

    clog(f"emailserver: add email handled (added {add_email})")


def remove_email_query_handler(_query):
    global AUTHORIZED_EMAILS_LIST_FILE_PATH
    global AUTHORIZED_EMAILS_LIST

    global ADMIN_EMAIL

    remove_email = _query.query_data["remove_email"]

    alias_tmp = None

    if remove_email in AUTHORIZED_EMAILS_LIST.keys():
        alias_tmp = AUTHORIZED_EMAILS_LIST[remove_email]["alias"]
        del AUTHORIZED_EMAILS_LIST[remove_email]
        file = open(AUTHORIZED_EMAILS_LIST_FILE_PATH, "w")
        json.dump(AUTHORIZED_EMAILS_LIST, file, indent=4)

        email_interface.send_email(
            ADMIN_EMAIL,
            f"successful admin cmd execution notice",
            f"deauthorized {remove_email} ({alias_tmp})\n",
        )
    else:
        email_interface.send_email(
            ADMIN_EMAIL,
            f"unsuccessful admin cmd execution notice",
            f"unable to deauthorize {remove_email}: not found\n",
        )

    file.close()

    clog(
        f"emailserver: remove email handled (attempted to remove {remove_email})"
    )


def nuke_email_query_handler(_query):
    pass


def show_authorized_email_query_handler(_query):
    global AUTHORIZED_EMAILS_LIST

    global ADMIN_EMAIL

    email_interface.send_email(
        ADMIN_EMAIL,
        f"successful admin cmd execution notice",
        f"authorized users list:\n{json.dumps(AUTHORIZED_EMAILS_LIST, indent=4)}\n",
    )

    clog(f"emailserver: authorized emails list provided")


# format:
# kwargs present:
# origin and o=[s and sinchon or i and songdo and internaitonal]
# date and d=[mmdd or yyyymmdd] verbal: tomorrow, overmorrow, next friday this friday etc..
# time and t=[hh:mm]
# (optional) mode=[r or l]
# kwargs not present:
# origin date time mode
def book_email_query_handler(_query):
    global NOW
    global QUERY_PREFIX

    def book_email_query_details_parser(details):
        def verbal_interpret(argument, _today):
            today_weekday = _today.weekday()

            argument = argument.lower()

            if argument == "td" or argument == "today":
                return 0
            elif (
                argument == "tmo" or argument == "tmr" or argument == "tomorrow"
            ):
                return 1
            elif argument == "ovm" or argument == "overmorrow":
                return 2

            # 7 but zero indexed so 6 days a week
            argument = list(argument)  # gotta be fast
            argument.reverse()

            next_cnt = 0
            delta = 6 - today_weekday
            cache = ""
            while len(argument) != 0:
                letter = argument.pop()
                cache += letter

                if cache == "next":
                    delta += 7
                    cache = ""
                elif cache == "mon":
                    delta += 1
                    return delta
                elif cache == "tue":
                    delta += 2
                    return delta
                elif cache == "wed":
                    delta += 3
                    return delta
                elif cache == "thu":
                    delta += 4
                    return delta
                elif cache == "fri":
                    delta += 5
                    return delta
                elif cache == "sat":
                    delta += 6
                    return delta
                elif cache == "sun":
                    delta += 7
                    return delta
                elif len(cache) >= 5:
                    return ValueError()

            return delta

        try:
            today = datetime.date.today()

            today_year = today.year
            today_month = today.month
            today_day = today.day

            parsed_origin = None
            parsed_date = None
            parsed_time = None
            parsed_mode = "l"

            assembly_year = 0
            assembly_month = 0
            assembly_day = 0

            assembly_hour = 0
            assembly_minute = 0

            # kwarg mode
            if "=" in details:
                args = details.split(" ")
                i = 0
                while i < len(args):
                    if args[i] == "":
                        del args[i]
                    else:
                        i += 1

                i = 0
                while i < len(args):
                    args[i] = args[i].split("=")
                    i += 1

                for kwarg in args:
                    if len(kwarg) < 2:
                        return (
                            "keyword argument error",
                            "malformed keyword argument",
                        )
                    kwarg[0] = kwarg[0].lower()
                    if kwarg[0] == "o" or kwarg[0] == "origin":
                        parsed_origin = kwarg[1]
                    elif kwarg[0] == "d" or kwarg[0] == "date":
                        parsed_date = kwarg[1]
                    elif kwarg[0] == "t" or kwarg[0] == "time":
                        parsed_time = kwarg[1]
                    elif kwarg[0] == "m" or kwarg[0] == "mode":
                        parsed_mode = kwarg[1]
                    else:
                        return (
                            "keyword argument error",
                            f"unknown keyword argument: {kwarg[0]}",
                        )

                if parsed_origin is None:
                    return ("keyword argument error", "origin not supplied")
                if parsed_date is None:
                    return ("keyword argument error", "date not supplied")
                if parsed_time is None:
                    return ("keyword argument error", "time not supplied")

            # no kwarg mode
            else:
                args = details.split(" ")
                i = 0
                while i < len(args):
                    if args[i] == "":
                        del args[i]
                    else:
                        i += 1

                if len(args) < 3:
                    return ("sequential arguments error", "insufficient args")
                parsed_origin = args[0]
                parsed_date = args[1]
                parsed_time = args[2]
                if len(args) >= 4:
                    parsed_mode = args[3]

            parsed_origin = parsed_origin.lower()
            parsed_date = parsed_date.lower()
            parsed_time = parsed_time.lower()
            parsed_mode = parsed_mode.lower()

            # parse args sinchon songdo
            if parsed_origin == "sinchon" or parsed_origin == "s":
                parsed_origin = "S"
            elif (
                parsed_origin == "international"
                or parsed_origin == "i"
                or parsed_origin == "songdo"
            ):
                parsed_origin = "I"
            else:
                return ("interpretation error", "malformed origin")

            if parsed_mode == "left" or parsed_mode == "l":
                parsed_mode = "l"
            elif parsed_mode == "right" or parsed_mode == "r":
                parsed_mode = "r"
            else:
                return ("interpretation error", "malformed origin")

            try:
                verbal = False
                for c in parsed_date:
                    if not c.isdigit():
                        verbal = True
                        break

                if verbal:
                    delta = verbal_interpret(parsed_date, today)
                    if isinstance(delta, ValueError):
                        return (
                            "interpretation error",
                            "verbal interpretation error",
                        )
                    shifted_date = today + datetime.timedelta(days=delta)
                    assembly_year = shifted_date.year
                    assembly_month = shifted_date.month
                    assembly_day = shifted_date.day
                else:
                    if len(parsed_date) == 4:
                        assembly_month = int(parsed_date[0:2])
                        assembly_day = parsed_date[2:4]
                        if assembly_month < today_month:
                            assembly_year = today_year + 1
                        else:
                            assembly_year = today_year
                    elif len(parsed_date) == 8:
                        assembly_year = parsed_date[0:4]
                        assembly_month = parsed_date[4:6]
                        assembly_day = parsed_date[6:8]
                    else:
                        return ("interpretation error", "malformed date")
            except Exception as ex:
                return ex

            try:
                assembly_hour = parsed_time[0:2]
                assembly_minute = parsed_time[2:4]
            except Exception:
                return ("interpretation error", "malformed time")

            try:
                parsed_date_time = datetime.datetime(
                    int(assembly_year),
                    int(assembly_month),
                    int(assembly_day),
                    int(assembly_hour),
                    int(assembly_minute),
                )
                if parsed_date_time < datetime.datetime.now():
                    return ("invalidity error", "date has passed")
                else:
                    return [parsed_origin, parsed_date_time, parsed_mode]
            except Exception as ex:
                return (
                    "interpretation error",
                    "datetime object interpretaiton error",
                )

        except Exception as ex:
            return ("unknown error", "unknown runtime error")

    id = _query.query_data["id"]
    pw = _query.query_data["pw"]

    # create "virtual" user
    _query.query_data["user"] = User(
        id, pw, _auth_on_init=False, _email_query=_query
    )

    credential_validity = check_credentials(_query.query_data["user"])

    if not credential_validity:
        email_interface.send_email(
            _query.sender_email,
            f"😅 your request could not be accepted",
            f"your request made at {_query.recv_datetime.strftime('%c')} was not accepted because your request had errors in it:\n"
            f"\n"
            f"your id (학번) or/and passwords were not correct (probably) if you are a 100%\n"
            f"sure that your credentials were correct, please contact administrator\n",
        )
        return

    # store book details
    book_details = _query.query_data["book_details"]

    # try interpreting book details
    result = book_email_query_details_parser(book_details)
    # if len is two we probably got an error outcome
    if len(result) == 2:
        # show error message
        clog(f"emailserver: book request couldnt be fullfilled: {result}")
        email_interface.send_email(
            _query.sender_email,
            f"😥 your request could not be accepted",
            f"your request made at {_query.recv_datetime.strftime('%c')} was not accepted because your request had errors in it:\n"
            f"\n"
            f"you probably messed up the booking details argument, please consult the\n"
            f"user manual, that can be requested by sending an email with an empty body\n",
        )
    # else we try making further moves
    else:
        _query.query_data["book_arguments"] = {}
        _query.query_data["book_arguments"]["origin"] = result[0]
        _query.query_data["book_arguments"]["departure_datetime"] = result[
            1
        ].strftime("%F %T")
        _query.query_data["book_arguments"]["mode"] = result[2]

        r = WishlistRoute(
            _query.query_data["user"], result[0], result[1], result[2]
        )

        # insert in user book queue for email server
        insert_route_BOOK_QUEUE_EMAIL_SERVER(r)
        clog(f"emailserver: wishlist route added to emailserver's book queue")
        email_interface.send_email(
            _query.sender_email,
            f"😊 your request ({r.__str__(official=True)}) was accepted",
            f"your request made at {_query.recv_datetime.strftime('%c')} was accepted and added to the emailserver's book queue, wrote to local memory.\n"
            f"request details:\n"
            f"origin: {r.origin}\n"
            f"departure date & time: {r.departure_datetime.strftime('%c')}\n"
            f"booking mode: {r.mode}\n"
            f"\n"
            f"when the appropriate time comes the booking request will be automatically handled\n"
            f"on our side, we will send you another email when the actual reservation will be carried out 😊",
        )

        serialized_query = _query.serialize()

        #'{:_<10}'.format('test')
        # test______

        dirs = os.listdir(BOOK_QUERIES_PATH_LOOKUP_DICT[_query.sender_email])
        index = 0

        if len(dirs) == 0:
            index_formatted = "{:0>2}".format(int(0))
            file = open(
                f"{BOOK_QUERIES_PATH_LOOKUP_DICT[_query.sender_email]}/{QUERY_PREFIX + index_formatted}.json",
                "w",
            )
            json.dump(serialized_query, file, indent=4)
            file.close()
        else:
            i = 0
            while i < len(dirs):
                dirs[i] = int(dirs[i].split("_")[1][:-5])
                i += 1

            i = 0
            j = 0
            while i < len(dirs):
                if j < dirs[i]:
                    break
                i += 1
                j += 1

            index_formatted = "{:0>2}".format(int(j))
            index = j
            file = open(
                f"{BOOK_QUERIES_PATH_LOOKUP_DICT[_query.sender_email]}/{QUERY_PREFIX + index_formatted}.json",
                "w",
            )
            json.dump(serialized_query, file, indent=4)
            file.close()

        _query.index = index

        # book whatever is possible in email server book queue
        book_available_email_server(NOW)


def show_email_query_handler(_query):
    pass


def delete_email_query_handler(_query):
    pass


def invalid_email_query_handler(_query):
    email_interface.send_email(
        _query.sender_email,
        f"😅 your request was malformed",
        f"your request made at {_query.recv_datetime.strftime('%c')} was malformed, therfore discarded\n"
        f"(we literally couldn't understand what you are trying to do)\n\n"
        f"<b>there is a possibility that your email app inserted weird characters in your email</b>\n"
        f"here is what we received:\n"
        f">>>> START OF EMAIL MESSAGE >>>>\n"
        f"{_query.body}\n"
        f">>>> END OF EMAIL MESSAGE >>>>\n\n"
        f"if you see weird characters and misinterpretation on our side, please use "
        f"another email app or contact the administrator to get this mistake fixed...\n\n"
        f"<b>in case you need help, here is a guide on how to use this email address:</b>\n"
        f"1. email subjects can contain whatever you want, they are always discarded on arrival.\n"
        f"in the body of the email you shoud first write the command you want to execute, for example:\n"
        f"book, show, delete and etc...\n\n"
        f"2. after a command, 'arguments' might follow. each argument  must be on a separate line.\n"
        f"for example, the command book needs three arguments: your student ID (학번),\n"
        f"your yonsei portal password and a line that specifies booking details\n"
        f"\n\nexample body of a mail intended to use the command 'book':\n\n"
        f"<code>"
        f"book\n"
        f"2023123456\n"
        f"cool_password_123\n"
        f"sinchon nextmonday 0800 right"
        f"</code>\n\n\n"
        f"as you can see, the emails' bodies have to have everything on separate lines\n"
        f"3. now, we are going to explain the individual commands and explain what they do\n\n\n"
        f'<font size="+2">book:</font>\n'
        f"requests a shuttle bus booking. notice that the booking can be set to whatever time in future. "
        f"as long as the server runs and the bug on yonsei's website isn't patched the shuttle will be provided.\n"
        f"<b>bear in mind that this program cant book a shuttle if it is already full.</b>\n"
        f"<b>argumets for book:</b>\n"
        f"<code>"
        f"line01: your student ID (학번)\n"
        f"line02: your yonsei portal password\n"
        f"line03: booking details</code>\n\n"
        f"booking details can come in various forms:\n"
        f"there are three basic arguments (origin, date, time) and one additional (mode)\n"
        f"'origin' defines where does the shuttle bus departs from\n"
        f"'date' defines the date the shuttle bus deprats on <b>(has to be in format YYYYMMDD or MMDD!)</b>\n"
        f"'time' defines the time the shuttle bus departs at <b>(has to be in format HHMM!)</b>\n"
        f"'mode' defines whether the program should look for shuttle before or after the specified time:\n"
        f"if 'mode' is set to 'right' or 'r' the program will take a shuttle as close as possible to the\n"
        f"specified time but it will be after or exactly at it\n"
        f"if 'mode' is set to 'left' or 'l' the program will take a shuttle as close as possible to the\n"
        f"specified time but it will be before or exactly at it\n"
        f"you can specify argumets in the order, separated by spaces 'origin' 'date' 'time' 'mode'(omittable)\n"
        f"or you can specify argumets by explicitly telling the keyword, for example:\n"
        f"ex. 1:\n"
        f"origin=Sinchon date=1015 time=0730 mode=right\n"
        f"explanation: the server chooses a shuttle departs from sinchon and departs on the 15th of october\n"
        f"at 7:30 am or later\n"
        f"ex. 2: (keywords can be shortened to first letter)\n"
        f"m=r o=I d=tomorrow t=1930\n"
        f"explanation: we specified arguments in a random order, because we told the program which arguments\n"
        f"are what. note that '=' should have no spaces around it and the date was specified verbally.\n"
        f"I stands for international or songdo campus, S stands for sinchon campus.\n"
        f"dates can be specified by words like monday, tuesday, tomorrow, nextmonday, nextnextfriday and etc.\n\n\n"
        f'<font size="+2">show: NOT IMPLEMENTED YET</font>\n'
        f"shows currently requested shuttle busses.\n"
        f"arguments for show:\n"
        f"<there are no argments for show>\n\n\n"
        f'<font size="+1">NOW, important notice:</font>\n'
        f'<font size="+1"><b>CANCEL SHUTTLES YOU WONT RIDE!!</b></font>\n'
        f"seriously, dont be a prick. thanks 😊\n\n"
        f"made with ❤ by l.",
    )


def forbidden_email_query_handler(_query):
    email_interface.send_email(
        _query.sender_email,
        f"😅 your request is forbidden",
        f"your request made at {_query.recv_datetime.strftime('%c')} was forbidden, therfore discarded\n"
        f"why do you even know this...?\n",
    )


# endregion


# region email server main funcs


def email_server_upd():
    global EMAIL_SERVER_MESSAGE_READ_REFRESH_RATE
    global EMAIL_SERVER_MESSAGE_READ_BATCH_SIZE

    global EMAIL_QUERIES
    global EMAIL_QUERIES_PROCESSED
    global EMAIL_QUERIES_UNPROCESSED

    while True:
        time.sleep(EMAIL_SERVER_MESSAGE_READ_REFRESH_RATE)
        emails = email_interface.get_emails(
            _maxResults=EMAIL_SERVER_MESSAGE_READ_BATCH_SIZE, _unread=True
        )

        for i in range(len(emails)):
            query = EmailQuery(
                emails[i]["date"],
                emails[i]["subject"],
                emails[i]["sender_info"],
                emails[i]["body"],
            )
            EMAIL_QUERIES_UNPROCESSED.append(query)

        if len(EMAIL_QUERIES_UNPROCESSED) != 0:
            clog(f"got {len(emails)} new emails...")

        # work queries
        i = 0
        while len(EMAIL_QUERIES_UNPROCESSED) != 0:
            query = EMAIL_QUERIES_UNPROCESSED.pop()

            if query.query_data["type"] == "unauthorized":
                unauthorized_email_query_handler(query)
            elif query.query_data["type"] == "add":
                add_email_query_handler(query)
            elif query.query_data["type"] == "remove":
                remove_email_query_handler(query)
            elif query.query_data["type"] == "nuke":
                nuke_email_query_handler(query)
            elif query.query_data["type"] == "show_authorized":
                show_authorized_email_query_handler(query)
            elif query.query_data["type"] == "book":
                book_email_query_handler(query)
            elif query.query_data["type"] == "show":
                show_email_query_handler(query)
            elif query.query_data["type"] == "delete":
                delete_email_query_handler(query)
            elif query.query_data["type"] == "invalid":
                invalid_email_query_handler(query)
            elif query.query_data["type"] == "forbidden":
                forbidden_email_query_handler(query)
            else:
                raise LookupError("unrecognizable query data type retreived")


def email_server_startup():
    global AUTHORIZED_EMAILS_LIST
    global EMAIL_QUERIES
    global ADMIN_EMAIL

    # runopt
    global EMAIL_SERVER_BOOK_TIME

    global thread_email_server_upd
    global EMAIL_SERVER_CONFIG_FILE_PATH

    global DEFAULT_EMAIL_SERVER_CONFIG

    global BOOK_QUERIES_PATH_LOOKUP_DICT

    email_interface.initalize()

    # region email server config management
    if os.path.exists(EMAIL_SERVER_CONFIG_FILE_PATH):
        # region config load
        with open(EMAIL_SERVER_CONFIG_FILE_PATH, "r") as file:
            # try config opening
            try:
                # load config in general
                CONFIG = json.load(file)

                # run options load below
                RUNOPT = CONFIG["RUNOPT"]

                EMAIL_SERVER_BOOK_TIME = datetime.time(
                    *list(map(int, RUNOPT["EMAIL_SERVER_BOOK_TIME"].split(" ")))
                )

                ADMIN_EMAIL = RUNOPT["ADMIN_EMAIL"]

            # catch email server config errors
            except Exception as ex:
                cprint_(
                    f"error occured while reading email server config: {ex}"
                )
                exit()
        # endregion
    else:
        # region empty email server config generation
        with open(EMAIL_SERVER_CONFIG_FILE_PATH, "w+") as file:
            CONFIG = DEFAULT_EMAIL_SERVER_CONFIG
            json.dump(DEFAULT_EMAIL_SERVER_CONFIG, file)
            clog(
                f"default config file generated: {CONFIG}\n"
                "IMPORTANT: CONFIG BEFORE RESTARTING!!"
            )
            exit()
        # endregion
    clog(f"email server config loaded: {CONFIG}")
    # endregion

    # region allowed_emails_list management
    if os.path.exists(AUTHORIZED_EMAILS_LIST_FILE_PATH):
        # region allowed emails load
        with open(AUTHORIZED_EMAILS_LIST_FILE_PATH, "r") as file:
            AUTHORIZED_EMAILS_LIST = json.load(file)
            if ADMIN_EMAIL not in AUTHORIZED_EMAILS_LIST.keys():
                clog(
                    "admin email wasnt found in allowed email list. aborting launch..."
                )
                exit()
        # endregion
        clog(f"allowed emails retreived: {AUTHORIZED_EMAILS_LIST}")

        dirs = os.listdir(BOOK_QUERIES_SUBFLODER_PATH)

        for email in AUTHORIZED_EMAILS_LIST.keys():
            path = BOOK_QUERIES_SUBFLODER_PATH + "\\" + email
            if email not in dirs:
                os.mkdir(path)
                clog(
                    f"emailserver: created book queries storage directory for {email}"
                )
            BOOK_QUERIES_PATH_LOOKUP_DICT[email] = path
            clog(f"emailserver: added email to BOOK_QUERIES_PATH_LOOKUP_DICT")

    else:
        # region empty allowed emails list generation
        with open(AUTHORIZED_EMAILS_LIST_FILE_PATH, "w+") as file:
            AUTHORIZED_EMAILS_LIST = DEFAULT_ALLOWED_EMAIL_LIST
            json.dump(DEFAULT_ALLOWED_EMAIL_LIST, file)
            clog("allowed emails list created... but its empty, configure it")
        # endregion
    # endregion

    # region email_query management
    # load stored queries

    dirs = os.listdir(BOOK_QUERIES_SUBFLODER_PATH)

    for email in dirs:
        queries = os.listdir(f"{BOOK_QUERIES_SUBFLODER_PATH}/{email}")
        for query in queries:
            full_path = f"{BOOK_QUERIES_SUBFLODER_PATH}/{email}/{query}"
            file = open(full_path, "r")
            serialized_data = json.load(file)

            query_index = int(query.split("_")[1][:-5])

            # pass arbitrary data
            query = EmailQuery(None, None, None, None)
            query.load(serialized_data)
            query.index = query_index

            r = WishlistRoute(
                query.query_data["user"],
                query.query_data["book_arguments"]["origin"],
                query.query_data["book_arguments"]["departure_datetime"],
                query.query_data["book_arguments"]["mode"],
            )

            file.close()

            insert_route_BOOK_QUEUE_EMAIL_SERVER(r)
    book_available_email_server(NOW)
    # endregion

    # start server
    thread_email_server_upd = threading.Thread(target=email_server_upd)
    thread_email_server_upd.daemon = True
    thread_email_server_upd.start()


# endregion

# endregion


# region main program main funcs


def clock_upd():
    """
    main function that drives the app
    """
    global NOW

    global SHTTL_MPS
    global CONSOLE
    global DAYS_FROM_START
    global UPDATING_LOCK

    global ACTIVE_USER

    global thread_email_server_upd

    currd = NOW.day
    last_map_update = NOW
    flag = False
    flag_email = False

    while True:
        time.sleep(REFRESH_RATE_CLOCK)
        NOW = datetime.datetime.now()
        t_from_last_map_update = NOW - last_map_update

        # every REFRESH_RATE_SHTTL_LST seconds update SHTTL_LST
        if t_from_last_map_update.seconds > REFRESH_RATE_SHTTL_LST:
            UPDATING_LOCK = True
            users_exec(check_auth_and_exec, (update_SHTTL_LST, (NOW,)))
            UPDATING_LOCK = False
            last_map_update = NOW
            # clog("refreshed shuttle list", False)

        # execute schedule bookings when BOOK_TIME is surpassed
        if (
            not flag
            and NOW.hour >= BOOK_TIME.hour
            and NOW.minute >= BOOK_TIME.minute
            and NOW.second >= BOOK_TIME.second
        ):
            # try:
            # update next three days
            clog("updating SHTTL_LST", False)
            users_exec(check_auth_and_exec, (update_SHTTL_LST, (NOW,)))
            # book available routes
            clog("booking available routes in BOOK_QUEUE_SCDL", False)
            users_exec(
                check_auth_and_exec,
                (
                    book_available,
                    ("SCDL", NOW, False, 3),
                ),
            )
            users_exec(
                check_auth_and_exec,
                (
                    book_available,
                    ("USER", NOW, False, 3),
                ),
            )
            # except Exception as ex:
            #     clog(
            #         f"error occured while inserting scheduled bookings: {ex}", False)
            flag = True

        if EMAIL_SERVER:
            if (
                not flag_email
                and NOW.hour >= EMAIL_SERVER_BOOK_TIME.hour
                and NOW.minute >= EMAIL_SERVER_BOOK_TIME.minute
                and NOW.second >= EMAIL_SERVER_BOOK_TIME.second
            ):
                clog(
                    "emailserver: booking available routes in BOOK_QUEUE_EMAIL_SERVER"
                )
                book_available_email_server(NOW)
                flag_email = True

        # check if day has passed
        if currd < NOW.day:
            flag = False
            flag_email = False
            currd = NOW.day
            # get shuttle maps
            clog("getting shuttle maps", False)
            SHTTL_MPS = get_shttl_map_n_days(ACTIVE_USER, NOW, 3)
            clog("inserting scheduled bookings", False)
            # insert schedule booings
            users_exec(insert_schedule_bookings, (DAYS_FROM_START,))
            # update days from start
            DAYS_FROM_START += 1

        # restart emailserver if crashed
        if thread_email_server_upd is not None and not thread_email_server_upd.is_alive():
            thread_email_server_upd = threading.Thread(target=email_server_upd)
            thread_email_server_upd.daemon = True
            thread_email_server_upd.start()


def startup():
    global thread_clock_upd

    global CONSOLE
    global NOW
    global SHTTL_MPS
    global START_DAY
    global DEFAULT_SCHEDULE

    global USERS
    global ACTIVE_USER

    # region config file loaded
    global USERS
    global ACTIVE_USER

    global REFRESH_RATE_CLOCK
    global REFRESH_RATE_SHTTL_LST

    global BOOK_TIME
    global DAYS_FROM_START
    global AUTH_SESSION_LENGTH

    global DEBUG
    global CLEAN_SCHEDULE
    # endregion

    # init console
    CONSOLE = Console(stderr=True)
    CONSOLE.print(
        "Yonsei shuttle bus command line tool",
        f"ver. {VERSION}",
        style="bold red",
    )

    # region config management
    if os.path.exists(CONFIG_FILE_PATH):
        # region config load
        with open(CONFIG_FILE_PATH, "r") as file:
            # try config opening
            try:
                # load config in general
                CONFIG = json.load(file)

                # users load below
                USER_DATA = CONFIG["USER_CREDENTIALS"]
                keys = USER_DATA.keys()

                for key in keys:
                    usr_index = int(key.split("_")[1])
                    usr = User(
                        USER_DATA[key]["USERID"],
                        USER_DATA[key]["USERPW"],
                        usr_index,
                        USER_DATA[key]["ALIAS"],
                    )
                    USERS.append(usr)

                # run options load below
                RUNOPT = CONFIG["RUNOPT"]

                REFRESH_RATE_CLOCK = RUNOPT["REFRESH_RATE_CLOCK"]
                REFRESH_RATE_SHTTL_LST = RUNOPT["REFRESH_RATE_SHTTL_LST"]

                BOOK_TIME = datetime.time(
                    *list(map(int, RUNOPT["BOOK_TIME"].split(" ")))
                )
                DAYS_FROM_START = RUNOPT["DAYS_FROM_START"]
                AUTH_SESSION_LENGTH = RUNOPT["AUTH_SESSION_LENGTH"]

                DEBUG = RUNOPT["DEBUG"]
                CLEAN_SCHEDULE = RUNOPT["CLEAN_SCHEDULE"]
                IGNORE_3DAYS = RUNOPT["IGNORE_3DAYS"]
                RUN_MAINLOOP = RUNOPT["RUN_MAINLOOP"]
                EMAIL_SERVER = RUNOPT["EMAIL_SERVER"]

            # catch config errors
            except Exception as ex:
                cprint_(f"error occured while reading config: {ex}")
                exit()
        # endregion
    else:
        # region empty config generation
        with open(CONFIG_FILE_PATH, "w+") as file:
            CONFIG = DEFAULT_CONFIG
            json.dump(DEFAULT_CONFIG, file)
            clog(
                f"default config file generated: {CONFIG}\n"
                "IMPORTANT: FILL OUT USERID AND USERPW BEFORE RESTARTING!!"
            )
            exit()
        # endregion
    clog(f"config loaded: {CONFIG}")

    clog(
        "users loaded and parsed:\n"
        + "\n\n".join([str(x) for x in USERS])
        + "\n"
    )
    # endregion

    # region schedule management
    if os.path.exists(SCHEDULE_FILE_PATH):
        # region config load
        with open(SCHEDULE_FILE_PATH, "r") as file:
            SCHEDULE_CONFIG = json.load(file)
            SCHEDULES = SCHEDULE_CONFIG.keys()

            for key in SCHEDULES:
                usr_index = int(key.split("_")[1])
                index = search_user_with_id(usr_index)
                if index == -1:
                    clog(
                        f"schedule for {key} was not assigned because the corresponding user wasnt loaded (check config?)"
                    )
                else:
                    USERS[index].SCHEDULE = SCHEDULE_CONFIG[key]

            clog(
                "schdules loaded for each user:\n"
                + "\n".join([x.str_schedule() for x in USERS])
            )

            if CLEAN_SCHEDULE:
                for usr in USERS:
                    usr.SCHEDULE = EMPTY_SCHEDULE
                clog("schdules overridden (CLEAN_SCHEDLE set to true)" + "\n")
        # endregion
    else:
        # region empty schedule generation
        with open(SCHEDULE_FILE_PATH, "w+") as file:
            json.dump(DEFAULT_SCHEDULE, file)
            clog("default schdule file created")
        # endregion

    # endregion

    # set active user (duh..)
    ACTIVE_USER = USERS[0]
    clog("active user set:\n" + str(USERS[0]) + "\n")

    # set dates, times
    NOW = datetime.datetime.now()
    START_DAY = NOW.date()

    if EMAIL_SERVER:
        email_server_startup()

    if not RUN_MAINLOOP:
        return

    # check auth
    users_exec(check_auth_reauth, ())

    # fill user_info
    info = users_exec(get_user_info, ())
    i = 0
    while i < len(USERS):
        USERS[i].info = info[i]
        i += 1

    # startup SHTTL_LST
    users_exec(update_SHTTL_LST, (NOW,))

    # startup SHTTL_MPS
    SHTTL_MPS = get_shttl_map_n_days(ACTIVE_USER, NOW)

    # book 7 days ahead
    for usr in USERS:
        for i in range(3 if IGNORE_3DAYS else 0, DAYS_FROM_START):
            insert_schedule_bookings(usr, i)

    for usr in USERS:
        print(usr.SCHEDULE)

    # start clock thread
    thread_clock_upd = threading.Thread(target=clock_upd)
    thread_clock_upd.daemon = True
    thread_clock_upd.start()

    # start console
    clog("starting console", main=False)
    console_handler()


# endregion

if __name__ == "__main__":
    startup()

    # eq = EmailQuery(
    #     datetime.datetime(2023, 10, 15, 12, 0, 0),
    #     "subject",
    #     {"sender_name": "luigi", "sender_email": ADMIN_EMAIL},
    #     "book\nid\npw\nS 20231016 1900 r",
    # )
    # print(eq)
    # book_email_query_handler(eq)
