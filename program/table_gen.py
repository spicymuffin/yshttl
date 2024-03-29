from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns


def gen_shttl_lst_table(_shttl_lst):
    table = Table(title="SHTTL_LST")
    mxI = -1
    mxS = -1
    for i in range(len(_shttl_lst)):
        table.add_column(f"{_shttl_lst[i]['date']} times")
        table.add_column("origin")
        table.add_column("# seats")
        if mxI < len(_shttl_lst[i]["I"]):
            mxI = len(_shttl_lst[i]["I"])
        if mxS < len(_shttl_lst[i]["S"]):
            mxS = len(_shttl_lst[i]["S"])

    for j in range(mxI):
        clmn = []
        for i in range(len(_shttl_lst)):
            if len(_shttl_lst[i]["I"]) > j:
                clmn.append(
                    str(_shttl_lst[i]["I"][j].departure_datetime.time())
                )
                clmn.append("I")
                clmn.append(str(_shttl_lst[i]["I"][j].seats_available))
            else:
                for i in range(3):
                    clmn.append("-")
        table.add_row(*clmn)

    table.add_section()

    for j in range(mxS):
        clmn = []
        for i in range(len(_shttl_lst)):
            if len(_shttl_lst[i]["S"]) > j:
                clmn.append(
                    str(_shttl_lst[i]["S"][j].departure_datetime.time())
                )
                clmn.append("S")
                clmn.append(str(_shttl_lst[i]["S"][j].seats_available))
            else:
                for i in range(3):
                    clmn.append("-")
        table.add_row(*clmn)
    return table


def gen_booked_shttl_lst_table(_booked_shttl_lst):
    table = Table(title="BOOKED_SHTTL_LST")
    mxI = -1
    mxS = -1
    table.add_column("#")
    for i in range(len(_booked_shttl_lst)):
        table.add_column(f"{_booked_shttl_lst[i]['date']} times")
        table.add_column("origin")
        if mxI < len(_booked_shttl_lst[i]["I"]):
            mxI = len(_booked_shttl_lst[i]["I"])
        if mxS < len(_booked_shttl_lst[i]["S"]):
            mxS = len(_booked_shttl_lst[i]["S"])

    for j in range(mxI):
        clmn = []
        clmn.append(str(j))
        for i in range(len(_booked_shttl_lst)):
            if len(_booked_shttl_lst[i]["I"]) > j:
                clmn.append(
                    str(_booked_shttl_lst[i]["I"][j].departure_datetime.time())
                )
                clmn.append("I")
            else:
                for i in range(2):
                    clmn.append("-")
        table.add_row(*clmn)

    table.add_section()

    for j in range(mxS):
        clmn = []
        clmn.append(str(j))
        for i in range(len(_booked_shttl_lst)):
            if len(_booked_shttl_lst[i]["S"]) > j:
                clmn.append(
                    str(_booked_shttl_lst[i]["S"][j].departure_datetime.time())
                )
                clmn.append("S")
            else:
                for i in range(2):
                    clmn.append("-")
        table.add_row(*clmn)
    return table


# TODO: implement this
def gen_shttl_lst_table_on_date(_shttl_lst, _date):
    for i in range(len(_shttl_lst)):
        if _date in _shttl_lst[i].keys():
            pass


# TODO: implement this
def gen_booked_shttl_lst_table_on_date(_shttl_lst, _date):
    for i in range(len(_shttl_lst)):
        if _date in _shttl_lst[i].keys():
            pass


def gen_book_queue_table(_book_queue):
    table = Table(title="book_queue")

    table.add_column("#")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("Origin")
    table.add_column("Mode")

    for i in range(len(_book_queue)):
        row = (
            str(i),
            str(_book_queue[i].departure_datetime.date()),
            str(_book_queue[i].departure_datetime.time()),
            _book_queue[i].origin,
            str(_book_queue[i].mode)
        )
        table.add_row(*row)

    return table


def gen_shttl_map_table(_shttl_map):
    """get shttl map table

    Args:
        _shttl_map (dict): shttl map

    Returns:
        table: table
    """
    table = Table(title=_shttl_map["date"])

    table.add_column("R. No.", style="cyan", no_wrap=True)
    table.add_column("Origin", style="green")
    table.add_column("Time", style="magenta")

    table.add_column("Origin", style="green")
    table.add_column("Time", style="magenta")

    for i in range(max(len(_shttl_map["S"]), len(_shttl_map["I"]))):
        table.add_row(
            str(i),
            "Sinchon" if i < len(_shttl_map["S"]) else "-",
            str(_shttl_map["S"][i].departure_datetime.time())
            if i < len(_shttl_map["S"])
            else "-",
            "International" if i < len(_shttl_map["I"]) else "-",
            str(_shttl_map["I"][i].departure_datetime.time())
            if i < len(_shttl_map["I"])
            else "-",
        )

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
    for i in range(len(_shttl_map["S"])):
        S.append(
            Panel(
                f"[b]#{i}[/b][yellow] {str(_shttl_map['S'][i].departure_datetime.time())}",
                expand=True,
                title_align="right",
            )
        )

    for i in range(len(_shttl_map["S"])):
        I.append(
            Panel(
                f"[b]#{i}[/b][yellow] {str(_shttl_map['I'][i].departure_datetime.time())}",
                expand=True,
                subtitle_align="right",
            )
        )

    return (Columns(S), Columns(I))
