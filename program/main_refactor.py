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

userid = "**replaced USERID using filter-repo**"
userpw = "**replaced PW using filter-repo**"
WMONID = ""
JSESSIONID = ""


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

    def __str__(self, verbose=1) -> str:
        if verbose:
            return f"""  date: {self.departure_datetime.date()}
  time: {self.departure_datetime.time()}
origin: {self.origin}
remdSt: {self.seats_available}"""
        else:
            return str(self.departure_datetime.time())

# endregion classes

console = Console()
console.print("Hello", "World!", style="bold red")




def get_SHTTL_MAP(_date):
    """get shttl map on date _date

    Args:
        _date (str): date in yyyymmdd format

    Returns:
        int: -1 on failure, 0 on success
    """
    global WMONID
    global JSESSIONID

    temp_lst_S = server_interface.get_shttl_list("S", _date)
    temp_lst_I = server_interface.get_shttl_list("I", _date)

    SHTTL_MAP = {"date": _date, "S": [], "I": []}

    for i in range(len(temp_lst_S)):
        rt = Route()
        rt.import_dictionary(temp_lst_S[i])
        SHTTL_MAP["S"].append(rt)

    for i in range(len(temp_lst_I)):
        rt = Route()
        rt.import_dictionary(temp_lst_I[i])
        SHTTL_MAP["I"].append(rt)

    # print(SHTTL_DICT)

    return SHTTL_MAP

WMONID, JSESSIONID = auth_master.get_auth_cookies(userid, userpw)

server_interface.WMONID = WMONID
server_interface.JSESSIONID = JSESSIONID

a = get_SHTTL_MAP("20230427")

rprint(a)


import json
from urllib.request import urlopen

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


def get_content(user):
    """Extract text from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"
    return f"[b]{name}[/b]\n[yellow]{country}"


console = Console()


users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
user_renderables = [Panel(get_content(user), expand=True) for user in users]
console.print(Columns(user_renderables))