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

# region file management
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME
# endregion

# region credentials
USERID = "**replaced USERID using filter-repo**"
USERPW = "**replaced PW using filter-repo**"
WMONID = ""
JSESSIONID = ""
# endregion

# region refresh rates
REFRESH_RATE_CLOCK = 1/4  # in seconds
REFRESH_RATE_SHTTL_LST = 30
# endregion

BOOK_TIME = datetime.time(0, 2, 0)
DAYS_FROM_START = 7
START_DAY = None
LAST_AUTH_TIME = datetime.datetime(1999, 1, 1, 0, 0, 0)
AUTH_SESSION = 60 * 5


CONSOLE = None
SCHEDULE = None

SHTTL_LST = []
SHTTL_MPS = []

thread_clock_upd = None

BOOK_QUEUE_SCDL = []
BOOK_QUEUE_USER = []

UPDATING_LOCK = False


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
    """print in console

    Args:
        msg (str): message
        main (bool, optional): whether run from main thread. Defaults to True.
    """
    global CONSOLE

    s = str(msg)
    s = s.replace('\n', '\n    ')
    if main:
        CONSOLE.print("[bold red]>>> [/]" + s)
    else:
        CONSOLE.print("[bold red]\n>>> [/]" + s)
        CONSOLE.print("[bold green]<<< [/]", end="")


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

    s = str(msg)
    if main:
        CONSOLE.log(s)
    else:
        CONSOLE.print()
        CONSOLE.log(s)
        CONSOLE.print("[bold green]<<< [/]", end="")


def cinput(indent=False):
    """get input from user

    Args:
        indent (bool, optional): whether to indent input. Defaults to False.

    Returns:
        str: user input
    """
    global CONSOLE

    if not indent:
        return CONSOLE.input("[bold green]<<< [/]")
    else:
        return CONSOLE.input("[bold green]    <<< [/]")
# endregion


# region classes
class WishlistRoute:
    """represent wishlisted routes
    """

    def __init__(self, _origin="S", _departure_datetime=datetime.datetime.now(), _mode="r") -> None:
        self.origin = _origin
        self.departure_datetime = _departure_datetime
        self.str_departure_date = datetime_to_str_date(_departure_datetime)
        self.str_departure_time = datetime_to_str_time(_departure_datetime)
        self.mode = _mode

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


# region auth
def check_auth_and_exec(func, args, force=False):
    """check authorization cookies for validity and execute func with arguments args

    Args:
        func (function): function to be executed
        args (tuple): parameters for function
        force (bool, optional): force reauthorization. Defaults to False.

    Returns:
        unknown: return value of func
    """
    global LAST_AUTH_TIME
    global NOW
    global WMONID
    global JSESSIONID

    if force or (NOW - LAST_AUTH_TIME).seconds > AUTH_SESSION:
        if force or not server_interface.check_login():
            cookies = auth_master.get_auth_cookies(USERID, USERPW)
            if isinstance(cookies, Exception):
                clog(f"auth_master failed to authenticate: {cookies}")
                return cookies
            with open(COOKIE_JAR_FILE_PATH, 'w') as file:
                file.write(cookies[0] + '\n' + cookies[1])
            WMONID, JSESSIONID = cookies
            server_interface.WMONID = WMONID
            server_interface.JSESSIONID = JSESSIONID
            clog("re-authenticated", False)

    return func(*args)


def check_auth_reauth(force=False):
    """check authorization cookies for validity

    Args:
        force (bool, optional): force reauthorization. Defaults to False.
    """
    global LAST_AUTH_TIME
    global NOW
    global WMONID
    global JSESSIONID

    if force or (NOW - LAST_AUTH_TIME).seconds > AUTH_SESSION:
        if force or not server_interface.check_login():
            cookies = auth_master.get_auth_cookies(USERID, USERPW)
            if isinstance(cookies, Exception):
                clog(f"auth_master failed to authenticate: {cookies}")
                return cookies
            with open(COOKIE_JAR_FILE_PATH, 'w') as file:
                file.write(cookies[0] + '\n' + cookies[1])
            WMONID = cookies[0]
            JSESSIONID = cookies[1]
            server_interface.WMONID = WMONID
            server_interface.JSESSIONID = JSESSIONID
            clog("re-authenticated", False)

    return (WMONID, JSESSIONID)
# endregion


# region shttl_map_management
def get_shttl_map(_date):
    """get shttl map on date _date

    Args:
        _date (str): date in yyyymmdd format

    Returns:
        dict: shttl_map
    """
    global WMONID
    global JSESSIONID

    temp_lst_S = server_interface.get_shttl_list('S', _date)
    temp_lst_I = server_interface.get_shttl_list('I', _date)

    shttl_map = {'date': _date, "S": [], 'I': []}

    for i in range(len(temp_lst_S)):
        rt = Route()
        rt.import_dictionary(temp_lst_S[i])
        # rprint(rt.dct)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        shttl_map['S'].append(rt)

    for i in range(len(temp_lst_I)):
        rt = Route()
        rt.import_dictionary(temp_lst_I[i])
        shttl_map['I'].append(rt)

    return shttl_map


def get_shttl_map_n_days(_now, n=3):
    """get a list of shttl_maps n days from _now

    Args:
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
        maps.append(get_shttl_map(days[i]))

    return maps
# endregion


# region pretty output
def gen_shttl_lst_table(_shttl_lst):
    table = Table(title="SHTTL_LST")
    mxI = -1
    mxS = -1
    for i in range(len(_shttl_lst)):
        table.add_column(f"{_shttl_lst[i]['date']} times")
        table.add_column("origin")
        table.add_column("# seats")
        if mxI < len(_shttl_lst[i]['I']):
            mxI = len(_shttl_lst[i]['I'])
        if mxS < len(_shttl_lst[i]['S']):
            mxS = len(_shttl_lst[i]['S'])

    cprint(mxI, mxS)
    for j in range(mxI):
        clmn = []
        for i in range(len(_shttl_lst)):
            if len(_shttl_lst[i]['I']) > j:
                clmn.append(
                    str(_shttl_lst[i]['I'][j].departure_datetime.time()))
                clmn.append('I')
                clmn.append(str(_shttl_lst[i]['I'][j].seats_available))
            else:
                for i in range(3):
                    clmn.append('-')
        table.add_row(*clmn)

    table.add_section()

    for j in range(mxS):
        clmn = []
        for i in range(len(_shttl_lst)):
            if len(_shttl_lst[i]['S']) > j:
                clmn.append(
                    str(_shttl_lst[i]['S'][j].departure_datetime.time()))
                clmn.append('S')
                clmn.append(str(_shttl_lst[i]['S'][j].seats_available))
            else:
                for i in range(3):
                    clmn.append('-')
        table.add_row(*clmn)
    return table


def gen_shttl_lst_table_on_date(_shttl_lst):
    pass


def gen_bookqueue_table(_book_queue):
    pass


def gen_shttl_map_table(_shttl_map):
    """get shttl map table

    Args:
        _shttl_map (dict): shttl map

    Returns:
        table: table
    """
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
    """gen shttl map panels

    Args:
        _shttl_map (dict): shttl map

    Returns:
        tuple: a tuple containing two column objects
    """
    S = []
    I = []
    for i in range(len(_shttl_map['S'])):
        S.append(Panel(
            f"[b]#{i}[/b][yellow] {str(_shttl_map['S'][i].departure_datetime.time())}", expand=True, title_align="right"))

    for i in range(len(_shttl_map['S'])):
        I.append(Panel(
            f"[b]#{i}[/b][yellow] {str(_shttl_map['I'][i].departure_datetime.time())}", expand=True, subtitle_align="right"))

    return (Columns(S), Columns(I))
# endregion


def insert_route_BOOK_QUEUE_SCDL(_route):
    """insert a schedule booking request into BOOK_QUEUE_SCDL (sorted)

    Args:
        _route (Route): route object that needs to be inserted
    """
    global BOOK_QUEUE_SCDL
    inserted = False
    for i in range(len(BOOK_QUEUE_SCDL)):
        if BOOK_QUEUE_SCDL[i].departure_datetime >= _route.departure_datetime:
            BOOK_QUEUE_SCDL.insert(i, _route)
            inserted = True
            return
    if inserted == False:
        BOOK_QUEUE_SCDL.append(_route)


def insert_route_BOOK_QUEUE_USER(_route):
    """insert a schedule booking request into BOOK_QUEUE_USER (sorted)

    Args:
        _route (Route): route object that needs to be inserted
    """
    global BOOK_QUEUE_USER
    inserted = False
    for i in range(len(BOOK_QUEUE_USER)):
        if BOOK_QUEUE_USER[i].departure_datetime >= _route.departure_datetime:
            BOOK_QUEUE_USER.insert(i, _route)
            inserted = True
            return
    if inserted == False:
        BOOK_QUEUE_USER.append(_route)


def insert_schedule_bookings(delta):
    """insert a schedule booking request into BOOK_QUEUE_SCDL on delta days from start of program

    Args:
        delta (int): # of days from start of the program
    """
    global START_DAY
    d = START_DAY + datetime.timedelta(days=delta)
    dow_i = d.weekday()
    rts = SCHEDULE[str(dow_i)]
    for j in rts:
        splt = j["time"].split(":")
        hours = int(splt[0])
        minutes = int(splt[1])
        rdt = datetime.datetime(d.year, d.month, d.day, hours, minutes)
        if rdt - datetime.timedelta(seconds=5) > NOW:
            wrt = WishlistRoute(j["origin"], rdt, j["mode"])
            insert_route_BOOK_QUEUE_SCDL(wrt)


def update_SHTTL_LST(_now):
    global SHTTL_LST
    """update SHTTL_LST assuming that only the next three days are available
    """
    SHTTL_LST = get_shttl_map_n_days(_now, 3)


def book_available(_book_queue, _now, main=False, n=3):
    global UPDATING_LOCK
    global SHTTL_MPS

    if len(_book_queue) == 0:
        return

    while _book_queue[0].departure_datetime + datetime.timedelta(seconds=5) < NOW:
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
        shttl_map = None
        for i in range(len(SHTTL_MPS)):
            if SHTTL_MPS[i]["date"] == rt.str_departure_date:
                shttl_map = SHTTL_MPS[i][rt.origin]
                break

        min_diff = 24*60*60  # max minutes in a day
        min_diff_index = None
        found = False

        for i in range(len(shttl_map)):
            if rt.mode == 'r':  # switch timestamp places so we find min dst before or after
                diff = shttl_map[i].departure_datetime.timestamp() - \
                    rt.departure_datetime.timestamp()
            else:
                diff = rt.departure_datetime.timestamp() -  \
                    shttl_map[i].departure_datetime.timestamp()

            if min_diff > diff and shttl_map[i].seats_available > 0 and diff >= 0:
                min_diff_index = i
                min_diff = diff
                found = True

        if found:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            shttl_map[min_diff_index].book()
            if rt.mode == "l":
                cprint(f"""successfully booked shttl before (L) {rt.departure_datetime.time()}:
  origin: {shttl_map[min_diff_index].origin}
    date: {shttl_map[min_diff_index].departure_datetime.date()}
    time: {shttl_map[min_diff_index].departure_datetime.time()}""", main)
            else:
                cprint(f"""successfully booked shttl after (R) {rt.departure_datetime.time()}:
  origin: {shttl_map[min_diff_index].origin}
    date: {shttl_map[min_diff_index].departure_datetime.date()}
    time: {shttl_map[min_diff_index].departure_datetime.time()}""", main)
            _book_queue.pop(0)
        else:
            cprint(f"""failed to book shttl:
  origin: {rt.origin}
    date: {rt.departure_datetime.date()}
    time: {rt.departure_datetime.time()}""", main)
            _book_queue.pop(0)
        if len(_book_queue) > 0:
            rt = _book_queue[0]
        else:
            break


def clock_upd():
    """
    main function that drives the app
    """
    global NOW
    global SHTTL_LST
    global SHTTL_MPS
    global CONSOLE
    global DAYS_FROM_START
    global UPDATING_LOCK

    currd = NOW.day
    last_map_update = NOW
    flag = False

    while True:
        time.sleep(REFRESH_RATE_CLOCK)
        NOW = datetime.datetime.now()
        t_from_last_map_update = NOW - last_map_update
        # every REFRESH_RATE_SHTTL_LST seconds update SHTTL_LST
        if t_from_last_map_update.seconds > REFRESH_RATE_SHTTL_LST:
            UPDATING_LOCK = True
            check_auth_and_exec(update_SHTTL_LST, (NOW, ))
            UPDATING_LOCK = False
            last_map_update = NOW

        # execute schedule bookings when BOOK_TIME is surpassed
        if not flag and NOW.hour >= BOOK_TIME.hour \
                and NOW.minute >= BOOK_TIME.minute \
                and NOW.second >= BOOK_TIME.second:
            # try:
            # update next three days
            clog("updating SHTTL_LST", False)
            check_auth_and_exec(update_SHTTL_LST, (NOW, ))
            # book available routes
            clog("booking available routes in BOOK_QUEUE_SCDL", False)
            check_auth_and_exec(book_available, (BOOK_QUEUE_SCDL, NOW, ))
            # except Exception as ex:
            #     clog(
            #         f"error occured while inserting scheduled bookings: {ex}", False)
            flag = True
        if currd < NOW.day:
            flag = False
            currd = NOW.day
            # get shuttle maps
            clog("getting shuttle maps", False)
            SHTTL_MPS = get_shttl_map_n_days(NOW, 3)
            clog("inserting scheduled bookings", False)
            # insert schedule booings
            insert_schedule_bookings(DAYS_FROM_START)
            # update days from start
            DAYS_FROM_START += 1


# region commands
# region getcookies cmd
def getcookies_handler(args):
    with CONSOLE.status("updating lock....", spinner="clock"):
        ex = check_auth_reauth(force=True)
    if isinstance(ex, Exception):
        cprint(f"request couldnt be fullfilled: {ex}")
    else:
        cprint(f"cookies updated: {ex}")
# endregion


# region debug
def debug_handler(args):
    pass
    # global WMONID
    # global JSESSIONID
    # WMONID = "ASD"
    # JSESSIONID = "ASD"
    # server_interface.WMONID = WMONID
    # server_interface.JSESSIONID = JSESSIONID
    # check_auth_and_exec(check_book_queue, (NOW,))
# endregion


# region book cmd
def book_handler(args):
    global NOW
    args_processed = book_argument_parser(args)
    if type(args_processed) == str:
        # show error message
        cprint(f"request couldnt be fullfilled: {args_processed}")
    else:
        r = WishlistRoute(args_processed[0],
                          args_processed[1], args_processed[2])
        # insert in user book queue
        insert_route_BOOK_QUEUE_USER(r)
        cprint(f"route was added to wishlist successfully")
        # book whatever is possible in user book queue
        check_auth_and_exec(book_available, (BOOK_QUEUE_USER, NOW, True))


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
                return [origin, date_time, mode]
        except Exception as ex:
            return f"InvalidTimeError: DateTime invaild {ex}"

    except Exception as ex:
        cprint(f"request couldnt be fullfilled: {ex}")
# endregion


# region quit cmd
def quit_handler(args):
    cprint("quit? (type 'y' to confirm)")
    r = cinput(1)
    if r == 'y':
        quit(0)
# endregion


# region updshttllist cmd
def updshttllist_handler(args):
    global NOW
    global CONSOLE
    with CONSOLE.status("updating....", spinner="clock"):
        while UPDATING_LOCK:
            pass
        ex = check_auth_and_exec(update_SHTTL_LST, (NOW, ))
    if isinstance(ex, Exception):
        cprint(f"request couldnt be fullfilled: {ex}")
    else:
        cprint("SHTTL_LST updated")
# endregion


# region bookqueue cmd
def bookqueue_handler(args):
    table = None
    if len(args) == 1:
        table = gen_bookqueue_table(BOOK_QUEUE_USER)
    else:
        if args[2] == "u" or args[2] == "user":
            table = gen_bookqueue_table(BOOK_QUEUE_USER)
        elif args[2] == "s" or args[2] == "schedule":
            table = gen_bookqueue_table(BOOK_QUEUE_SCDL)
        else:
            cprint(f"request couldnt be fullfilled: invalid argument")

    if table != None:
        render(table)
# endregion


# region shttl_map cmd
def shttl_map_handler(args):
    global NOW
    table = None
    if len(args) == 1:
        table = gen_shttl_map_table(SHTTL_MPS[0])
    else:
        try:
            table = gen_shttl_map_table(SHTTL_MPS[str(args[1])])
        except Exception as ex:
            clog(f"request couldnt be fullfilled: {ex}")
    if table != None:
        render(table)
# endregion


# region shttl_lst cmd
def shttl_lst_handler(args):
    global NOW
    global SHTTL_LST
    if len(args) == 1:
        table = gen_shttl_lst_table(SHTTL_LST)
    else:
        try:
            table = gen_shttl_lst_table_on_date(SHTTL_LST)
        except Exception as ex:
            clog(f"request couldnt be fullfilled: {ex}")
    if table != None:
        render(table)
# endregion

# region clear cmd


def clear_handler(args):
    os.system('cls')
# endregion
# endregion


a**replaced ALIAS using filter-repo**s_book = ["book"]
a**replaced ALIAS using filter-repo**s_quit_handler = ["quit"]
a**replaced ALIAS using filter-repo**s_getcookies_handler = ["getcookies", "gc"]
a**replaced ALIAS using filter-repo**s_updshttllist = ["updshttllist", "updateshuttlelist", "usl"]
a**replaced ALIAS using filter-repo**s_bookqueue = ["bookqueue", "bq"]
a**replaced ALIAS using filter-repo**s_shttl_map = ["shttlmap", "sm", "shuttlemap"]
a**replaced ALIAS using filter-repo**s_clear = ["clear"]
a**replaced ALIAS using filter-repo**s_debug = ["db", "debug"]
a**replaced ALIAS using filter-repo**s_shttl_lst = ["shttllst", "sl", "shuttlelist"]


def tr_wrapper(func, args):
    if func == book_handler or func == shttl_map_handler:
        with CONSOLE.status("updating lock....", spinner="clock"):
            while UPDATING_LOCK:
                pass
    func(args)


def console_handler():
    while True:
        inp = cinput()
        inp_parsed = inp.split(" ")
        cmd = inp_parsed[0]
        exec = None
        if cmd in a**replaced ALIAS using filter-repo**s_book:
            exec = (book_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_quit_handler:
            exec = (quit_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_getcookies_handler:
            exec = (getcookies_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_updshttllist:
            exec = (updshttllist_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_bookqueue:
            exec = (bookqueue_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_shttl_map:
            exec = (shttl_map_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_clear:
            exec = (clear_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_debug:
            exec = (debug_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_shttl_lst:
            exec = (shttl_lst_handler, inp_parsed)
        else:
            cprint(f"{cmd} is not recognized as a command")
        if exec != None:
            tr_wrapper(exec[0], exec[1],)


def startup():
    global CONSOLE
    global SCHEDULE
    global thread_clock_upd
    global NOW
    global SHTTL_LST
    global SHTTL_MPS
    global START_DAY
    global LAST_AUTH_TIME

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

    # init console
    CONSOLE = Console(stderr=True)
    CONSOLE.print("Hello", "World!", style="bold red")

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
    for i in range(DAYS_FROM_START):
        insert_schedule_bookings(i)

    # start clock thread
    thread_clock_upd = threading.Thread(target=clock_upd)
    thread_clock_upd.daemon = True
    thread_clock_upd.start()

    # start console
    console_handler()


startup()
