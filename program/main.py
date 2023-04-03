import os
import threading
import time
import datetime
import auth_master
import server_interface
import json

# region file management
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME
# endregion

CLOCK_REFRESH_RATE = 1/4  # in seconds
SHTTL_DICT_REFRESH_RATE = 20
UPDATING_LOCK_NOTIFY_RATE = 1
NOW = None

USERID = "**replaced USERID using filter-repo**"
USERPW = "**replaced PW using filter-repo**"

WMONID = ""
JSESSIONID = ""

BOOK_QUEUE = []
SHTTL_DICT = {"S": {}, "I": {}}
UPDATING_LOCK = False

ENABLE_CONSOLE = 1
DEBUG = 1

FORCE_UPDATE_TIME = datetime.time(12, 0, 3)

SCHEDULE = {}
DAYS_FROM_START = 7
START_DAY = None

# region timetable format
# we need a system to set a schedule:
# timetable in config file:

"""
MON S 08:00
TUE
WED
THU
FRI I 10:00
SAT
SUN
"""
# use this ^ format to tell program which days it should automatically book bus
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


# region formatter functions
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
            return f"""  date: {self.departure_datetime.date()}
  time: {self.departure_datetime.time()}
origin: {self.origin}"""
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
        month = int(_dct["stdrDt"][5:6])
        day = int(_dct["stdrDt"][7:8])
        hour = int(_dct["beginTm"][0:2])
        minute = int(_dct["beginTm"][2:4])
        self.departure_datetime = datetime.datetime(
            year, month, day, hour, minute)
        self.seats_available = int(_dct["remndSeat"])

    def book(self):
        server_interface.book_shttl(self.dct)

    def __repr__(self):
        return str(self)

    def __str__(self, verbose=1) -> str:
        if verbose:
            return f"""  date: {self.departure_datetime.date()}
  time: {self.departure_datetime.time()}
origin: {self.origin}
remdSt: {self.seats_available}"""
        else:
            return str(self.departure_datetime.time())


def get_cookies():
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


def check_auth_and_exec(func, args):
    return func(*args)


def reset_SHTTL_DICT():
    global SHTTL_DICT
    SHTTL_DICT = {"S": {}, "I": {}}


def update_SHTTL_DICT(_date):
    """update internal representation of available routes on date _date

    Args:
        _origin (str): route origin S or I or B for both
        _date (str): date in yyyymmdd format

    Returns:
        int: -1 on failure, 0 on success
    """
    global WMONID
    global JSESSIONID

    temp_lst_S = server_interface.get_shttl_list("S", _date)
    temp_lst_I = server_interface.get_shttl_list("I", _date)

    for i in range(len(temp_lst_S)):
        rt = Route()
        rt.import_dictionary(temp_lst_S[i])
        if not _date in SHTTL_DICT["S"].keys():
            SHTTL_DICT["S"][_date] = []
        SHTTL_DICT["S"][_date].append(rt)

    for i in range(len(temp_lst_I)):
        rt = Route()
        rt.import_dictionary(temp_lst_I[i])
        if not _date in SHTTL_DICT["I"].keys():
            SHTTL_DICT["I"][_date] = []
        SHTTL_DICT["I"][_date].append(rt)

    # print(SHTTL_DICT)

    return 0


def update_n3d(_now):
    global UPDATING_LOCK

    tmr = _now + datetime.timedelta(days=1)
    ovm = _now + datetime.timedelta(days=2)
    str_tmr = datetime_to_str_date(tmr)
    str_ovm = datetime_to_str_date(ovm)
    str_td = datetime_to_str_date(_now)

    if UPDATING_LOCK:
        while UPDATING_LOCK:
            pass
        return (str_td, str_tmr, str_ovm)

    UPDATING_LOCK = True
    # TODO: we dont have to check login state literally every time

    reset_SHTTL_DICT()
    update_SHTTL_DICT(str_td)
    update_SHTTL_DICT(str_tmr)
    update_SHTTL_DICT(str_ovm)
    UPDATING_LOCK = False
    return (str_td, str_tmr, str_ovm)


def check_book_queue(_now):
    if not len(BOOK_QUEUE) > 0:
        cprint("BOOK_QUEUE empty")
        return

    j = 0
    while BOOK_QUEUE[j].departure_datetime + datetime.timedelta(seconds=5) < NOW:
        BOOK_QUEUE.pop(0)
        j += 1

    while UPDATING_LOCK:
        pass

    # print(SHTTL_DICT)

    tmr = _now + datetime.timedelta(days=1)
    ovm = _now + datetime.timedelta(days=2)
    str_td = datetime_to_str_date(_now)
    str_tmr = datetime_to_str_date(tmr)
    str_ovm = datetime_to_str_date(ovm)

    lst = [str_td, str_tmr, str_ovm]

    rt = BOOK_QUEUE[0]

    if rt.str_departure_date in lst:
        bs_lst = SHTTL_DICT[rt.origin][rt.str_departure_date]
        min_diff = 24*60*60  # max minutes in a day
        min_diff_index = None
        found = False
        for i in range(len(bs_lst)):
            diff = rt.departure_datetime.timestamp(
            ) - bs_lst[i].departure_datetime.timestamp()

            # print(diff, bs_lst[i].departure_datetime)

            # print(min_diff)
            # print(diff)
            # print(bs_lst[i].seats_available)

            # if min_diff > diff and bs_lst[i].seats_available == 0:
            #     print(f"rejected {bs_lst[i].departure_datetime.time()}")

            if min_diff > diff and bs_lst[i].seats_available > 0 and diff >= 0:
                min_diff_index = i
                min_diff = diff
                found = True

        if found:
            bs_lst[min_diff_index].book()
            cprint(f"""successfully booked shttl before {rt.departure_datetime.time()}:
    date: {bs_lst[min_diff_index].departure_datetime.date()}
    time: {bs_lst[min_diff_index].departure_datetime.time()}""")
            BOOK_QUEUE.pop(0)
        else:
            cprint(f"""failed to book shttl:
    date: {rt.departure_datetime.date()}
    time: {rt.departure_datetime.time()}""")


def insert_route_BOOK_QUEUE(_route):
    global BOOK_QUEUE
    inserted = False
    for i in range(len(BOOK_QUEUE)):
        if BOOK_QUEUE[i].departure_datetime >= _route.departure_datetime:
            BOOK_QUEUE.insert(i, _route)
            inserted = True
            return
    if inserted == False:
        BOOK_QUEUE.append(_route)


# region commands
# region getcookies cmd
def getcookies_handler(args):
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


# region debug
def debug_handler(args):
    pass
    check_auth_and_exec(check_book_queue, (NOW,))
# endregion


# region book cmd
def book_handler(args):
    global NOW
    args_processed = book_argument_parser(args)
    if type(args_processed) == str:
        cprint(f"request couldnt be fullfilled: {args_processed}")
    else:
        r = WishlistRoute(args_processed[0], args_processed[1])
        insert_route_BOOK_QUEUE(r)
        cprint(f"route was added to wishlist successfully")
        check_auth_and_exec(check_book_queue, (NOW, ))


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
                return [origin, date_time]
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
    now = datetime.datetime.now()
    r = check_auth_and_exec(update_n3d, (now, ))

    cprint(f"""Updated internal list:
    {r[0]}:
     S->I: {format(len(SHTTL_DICT['S'][r[0]]), "0>2") if r[0] in SHTTL_DICT['S'].keys() else "00"} shttls
     I->S: {format(len(SHTTL_DICT['I'][r[0]]), "0>2") if r[0] in SHTTL_DICT['I'].keys() else "00"} shttls
    {r[1]}:
     S->I: {format(len(SHTTL_DICT['S'][r[1]]), "0>2") if r[1] in SHTTL_DICT['S'].keys() else "00"} shttls
     I->S: {format(len(SHTTL_DICT['I'][r[1]]), "0>2") if r[1] in SHTTL_DICT['I'].keys() else "00"} shttls
    {r[2]}:
     S->I: {format(len(SHTTL_DICT['S'][r[2]]), "0>2") if r[2] in SHTTL_DICT['S'].keys() else "00"} shttls
     I->S: {format(len(SHTTL_DICT['I'][r[2]]), "0>2") if r[2] in SHTTL_DICT['I'].keys() else "00"} shttls""")
# endregion


# region bookqueue cmd
def bookqueue_handler(args):
    ps = ""
    for i in range(len(BOOK_QUEUE)):
        ps += f"    #{i}:\n"
        ps += f"datetime: {BOOK_QUEUE[i].departure_datetime}\n"
        ps += f"  origin: {BOOK_QUEUE[i].origin}"
        if i != len(BOOK_QUEUE) - 1:
            ps += '\n'
    cprint(ps)
# endregion


# region shttldict cmd
def shttldict_handler(args):
    ps = ""
    ps += "======== I ========\n"
    keys = list(SHTTL_DICT["I"].keys())
    for i in range(len(keys)):
        ps += f"{keys[i]}:\n"
        for j in range(len(SHTTL_DICT['I'][keys[i]])):
            ps += f"    bus #{j}:\n"
            ps += f"         time: {SHTTL_DICT['I'][keys[i]][j].departure_datetime.time()}\n"
            ps += f"        seats: {SHTTL_DICT['I'][keys[i]][j].seats_available}\n"

    ps += "======== S ========\n"
    keys = list(SHTTL_DICT["S"].keys())
    for i in range(len(keys)):
        ps += f"{keys[i]}:\n"
        for j in range(len(SHTTL_DICT['S'][keys[i]])):
            ps += f"    bus #{j}:\n"
            ps += f"         time: {SHTTL_DICT['S'][keys[i]][j].departure_datetime.time()}\n"
            ps += f"        seats: {SHTTL_DICT['S'][keys[i]][j].seats_available}\n"
    cprint(ps[:-1])
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
a**replaced ALIAS using filter-repo**s_shttldict = ["shttldict", "sd"]
a**replaced ALIAS using filter-repo**s_clear = ["clear"]
a**replaced ALIAS using filter-repo**s_debug = ["db", "debug"]


def tr_wrapper(func, args):
    if func == book_handler or func == shttldict_handler:
        while UPDATING_LOCK:
            cprint("locked. wait")
            time.sleep(UPDATING_LOCK_NOTIFY_RATE)
    func(args)


def console_handler():
    global CMD_QUEUE
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
        elif cmd in a**replaced ALIAS using filter-repo**s_shttldict:
            exec = (shttldict_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_clear:
            exec = (clear_handler, inp_parsed)
        elif cmd in a**replaced ALIAS using filter-repo**s_debug:
            exec = (debug_handler, inp_parsed)
        else:
            cprint(f"{cmd} is not recognized as a command")
        if exec != None:
            tr_wrapper(exec[0], exec[1],)


def book_schedule_from_sd(delta):
    global START_DAY
    d = START_DAY + datetime.timedelta(days=delta)
    dow_i = d.weekday()
    # print(d)
    rts = SCHEDULE[str(dow_i)]
    for j in rts:
        splt = j["time"].split(":")
        hours = int(splt[0])
        minutes = int(splt[1])
        rdt = datetime.datetime(d.year, d.month, d.day, hours, minutes)
        if rdt - datetime.timedelta(seconds=5) > NOW:
            rt = WishlistRoute(j["origin"], rdt)
            insert_route_BOOK_QUEUE(rt)


def clock_upd():
    global NOW
    global DAYS_FROM_START
    flag = False
    currd = NOW.day
    while True:
        time.sleep(CLOCK_REFRESH_RATE)
        NOW = datetime.datetime.now()

        # force update when 2pm happens bc thats the time
        # when new busses are added server-side
        if not flag and NOW.hour >= FORCE_UPDATE_TIME.hour \
                and NOW.minute >= FORCE_UPDATE_TIME.minute \
                and NOW.second >= FORCE_UPDATE_TIME.second:
            # update next three days
            check_auth_and_exec(update_n3d, (NOW, ))
            # check book_queue
            check_auth_and_exec(check_book_queue, (NOW, ))
            cprint("forced usl, checked bookings", main=False)
            flag = True
        if currd < NOW.day:
            flag = False
            currd = NOW.day
            book_schedule_from_sd(DAYS_FROM_START)
            DAYS_FROM_START += 1


def shttl_dict_upd():
    global NOW
    while True:
        time.sleep(SHTTL_DICT_REFRESH_RATE)
        #cprint("HELLO!!", main=False)
        check_auth_and_exec(update_n3d, (NOW, ))
        check_book_queue(NOW)


def startup():
    global NOW
    global START_DAY
    global SCHEDULE

    # region load cookies and config
    with open(CONFIG_FILE_PATH, 'r') as file:
        SCHEDULE = json.load(file)

    # print(SCHEDULE)

    if os.path.exists(COOKIE_JAR_FILE_PATH):
        with open(COOKIE_JAR_FILE_PATH, 'r') as file:
            WMONID = file.readline()[:-1]
            JSESSIONID = file.readline()

    server_interface.WMONID = WMONID
    server_interface.JSESSIONID = JSESSIONID
    # endregion

    if not server_interface.check_login():
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

    NOW = datetime.datetime.now()
    START_DAY = NOW.date()
    update_n3d(NOW)

    for i in range(DAYS_FROM_START):
        book_schedule_from_sd(i)

    thread_clock_upd = threading.Thread(target=clock_upd)
    thread_clock_upd.daemon = True
    thread_clock_upd.start()

    thread_shttl_dict_upd = threading.Thread(target=shttl_dict_upd)
    thread_shttl_dict_upd.daemon = True
    thread_shttl_dict_upd.start()

    # print(BOOK_QUEUE)


startup()

if DEBUG:
    #s = server_interface.get_shttl_list("S", "20230403")
    # print(s)
    pass


if ENABLE_CONSOLE:
    console_handler()

# requests code
# r = requests.get()
