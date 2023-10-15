# # # import requests

# # # cookies = {
# # #     'WMONID': 'gbmYHzPC3xQ',
# # #     'JSESSIONID': 'licewejSfPVwbUL4cElzhWbEoRnsTskqnjrTjW1j0HP999yax31akViWNxOR01aw.amV1c19kb21haW4vaGFrc2EyXzE=',
# # # }

# # # headers = {
# # #     'Accept': '*/*',
# # #     'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
# # #     'Connection': 'keep-alive',
# # #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# # #     # 'Cookie': 'WMONID=gbmYHzPC3xQ; _ga=GA1.3.748332228.1680069477; _gid=GA1.3.1219567376.1680069477; JSESSIONID=licewejSfPVwbUL4cElzhWbEoRnsTskqnjrTjW1j0HP999yax31akViWNxOR01aw.amV1c19kb21haW4vaGFrc2EyXzE=; _INSIGHT_CK_8301=80ac3f0625ecc11af35a81e06810a4e3_69476|27f33c18176930db719959265cd9a162_63391:1680165191000; cugubun=HYoNdPmyarAcCNUNVAAcCNVOaASQ; UbiResult=nyalIz1mdzeUGmDT1xnMJw==',
# # #     'Origin': 'https://underwood1.yonsei.ac.kr',
# # #     'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
# # #     'Sec-Fetch-Dest': 'empty',
# # #     'Sec-Fetch-Mode': 'cors',
# # #     'Sec-Fetch-Site': 'same-origin',
# # #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
# # #     'X-Requested-With': 'XMLHttpRequest',
# # #     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
# # #     'sec-ch-ua-mobile': '?0',
# # #     'sec-ch-ua-platform': '"Windows"',
# # # }

# # # data = '_findSavedRow=areaDivCd%2C%20busCd%2C%20seatNo%2C%20stdrDt%2C%20beginTm&_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23busCd=I5&%40d1%23busNm=5%ED%98%B8%EC%B0%A8&%40d1%23seatNo=&%40d1%23stdrDt=20230331&%40d1%23beginTm=0720&%40d1%23endTm=0820&%40d1%23tm=07%3A20%20~%2008%3A20&%40d1%23seatDivCd=&%40d1%23userDivCd=&%40d1%23persNo=&%40d1%23thrstNm=%EC%98%81%EC%A2%85%EB%8C%80%EA%B5%90%2C%20%EC%9D%B8%EC%B2%9C%EB%8C%80%EA%B5%90&%40d1%23remrk=&%40d1%23remndSeat=16&%40d1%23resveWaitPcnt=5&%40d1%23resveYn=0&%40d1%23resveWaitYn=0&%40d1%23resveResnDivCd=2&%40d1%23dailResvePosblYn=1&%40d1%23areaDivCd__origin=I&%40d1%23busCd__origin=I5&%40d1%23seatNo__origin=&%40d1%23stdrDt__origin=20230331&%40d1%23beginTm__origin=0720&%40d1%23sts=u&%40d%23=%40d1%23&%40d1%23=dsShtl110&%40d1%23tp=ds&%40d2%23gbn=P&%40d2%23seatDivCd=1&%40d2%23userDivCd=12&%40d%23=%40d2%23&%40d2%23=dmCond&%40d2%23tp=dm'

# # # response = requests.post(
# # #     'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/saveShtlbusResveList.do',
# # #     cookies=cookies,
# # #     headers=headers,
# # #     data=data,
# # # )

# # # print(response.content.decode())

# # # import datetime

# # # year = int(2023)
# # # month = int(3)
# # # day = int(5)
# # # hour = int(12)
# # # minute = int(23)
# # # departure_datetime = datetime.datetime(
# # #     year, month, day, hour, minute)

# # # print(departure_datetime)
# # # print(str(departure_datetime.year) + format(departure_datetime.month, "0>2") + format(departure_datetime.day, "0>2"))

# # # import requests

# # # cookies = {
# # #     'WMONID': 'mW5O3G11u0p',
# # #     'JSESSIONID': 'Jz1Q37zY1Dw7WdU1Fi7j8U3nRUlQwdbSz7KdmMbGkDZvb1XLxVvZVqaSu2HAJIBM.amV1c19kb21haW4vaGFrc2EyXzE=',
# # # }

# # # headers = {
# # #     'Accept': '*/*',
# # #     'Accept-Language': 'en-US,en;q=0.9',
# # #     'Connection': 'keep-alive',
# # #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# # #     # 'Cookie': 'WMONID=mW5O3G11u0p; JSESSIONID=Jz1Q37zY1Dw7WdU1Fi7j8U3nRUlQwdbSz7KdmMbGkDZvb1XLxVvZVqaSu2HAJIBM.amV1c19kb21haW4vaGFrc2EyXzE=',
# # #     'Origin': 'https://underwood1.yonsei.ac.kr',
# # #     'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
# # #     'Sec-Fetch-Dest': 'empty',
# # #     'Sec-Fetch-Mode': 'cors',
# # #     'Sec-Fetch-Site': 'same-origin',
# # #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
# # #     'X-Requested-With': 'XMLHttpRequest',
# # #     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
# # #     'sec-ch-ua-mobile': '?0',
# # #     'sec-ch-ua-platform': '"Windows"',
# # # }

# # # data = '_menuId=MzMzODYzMjY%3D&_menuNm=&_pgmId=MTg3NDA2&'

# # # response = requests.post(
# # #     'https://underwood1.yonsei.ac.kr/com/cnst/PropCtr/findViewSession.do',
# # #     cookies=cookies,
# # #     headers=headers,
# # #     data=data,
# # # )

# # # print(response.content.decode())


# # # import ast
# # # #                                                                                                                                                                                                                                                                          !                                                                              !
# # # r = '{"gdmViewSession":{"msg":"success","userNm":"꾸씩루이지","encStr":"SvRXCvYqst4AsjKIvDSVdnpTiByoar4knruU0j6e9y8=","deptNm":"컴퓨팅계열","locale":"locale","deptCd":"32053","deptTtNm":"컴퓨팅계열","userSupport":"0!@#undefined","clientDevice":"normal","passPwdExpir":True,"persNo":"**replaced USERID using filter-repo**","wasInfo":"운영","socpsCd":"1110","passLoginPolicy":True,"sessionTimeout":3600,"campsDivCd":"G","userDivCd":"12","reltmNtcnRcptnYn":"1","pageZoom":"100"},"dmLoginConfirm":{"isLogin":"1"}}'
# # # #r = '{"gay":True}'
# # # d0 = ast.literal_eval(r)
# # # print(d0)

# # # a = {"alen": 1, "**replaced ALIAS using filter-repo**": 2, "oleg": 3}

# # # for i in range(1, len(a.keys())):
# # #     print(a[a.keys()[i]])

# # # import datetime

# # # d1 = datetime.datetime(2023, 4, 1, 5, 45).timestamp()
# # # d2 = datetime.datetime(2023, 4, 1, 5, 44).timestamp()

# # # print((d2-d1))

# # # def a():
# # #     pass

# # # b = a

# # # print(b == a)

# # import datetime

# # dt = datetime.datetime.now()

# # for i in range(14):
# #     asd = dt + datetime.timedelta(days=i)
# #     print(asd.weekday())

# print("This message will remain in the console.")

# print("This is the message that will be deleted.", end="\r")

# import datetime
# print(datetime.datetime(2023, 2, 4, 9, 0, 0) + datetime.timedelta(days=100))

#!/usr/bin/python

# import time
# import subprocess
# import sys
# import msvcrt

# alarm1 = int(input("How many seconds (alarm1)? "))

# while (1):
#     time.sleep(alarm1)
#     print("Alarm1")
#     sys.stdout.flush()

# from io import StringIO
# from rich.console import Console
# console = Console(file=StringIO())
# console.print("[bold red]Hello[/] World")
# str_output = console.file.getvalue()
# console.print(str_output)


# class testclass:
#     def __init__(self, _name) -> None:
#         self.name = _name

#     def __str__(self) -> str:
#         return self.name

#     def __repr__(self) -> str:
#         return self.__str__()


# a = testclass("object1")

# list1 = []
# list2 = []

# list1.append(a)
# list2.append(a)

# print(list1)
# print(list2)

# a.name = "modified"
# b = a
# b.name = "modified twice"

# print(list1)
# print(list2)

# del list1[0]

# print(list1)
# print(list2)

# import os
# print(next(os.walk('C:/Users/**replaced ALIAS using filter-repo**/Desktop/github/yshttl/program/book_queries'))[1])

import datetime


def book_email_query_details_parser(details):
    def verbal_interpret(argument, _today):
        today_weekday = _today.weekday()

        argument = argument.lower()

        if argument == "td" or argument == "today":
            return 0
        elif argument == "tmo" or argument == "tmr" or argument == "tomorrow":
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
                if next_cnt != 0:
                    delta += 7
                next_cnt += 1
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
                    return ("kwarg", "malformed keyword argument")
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
                    return ("kwarg", f"unknown keyword argument: {kwarg[0]}")

            if parsed_origin is None:
                return ("kwarg", "origin not supplied")
            if parsed_date is None:
                return ("kwarg", "date not supplied")
            if parsed_time is None:
                return ("kwarg", "time not supplied")

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
                return ("orderedarg", "insufficient args")
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
            return ("interp", "malformed origin")

        if parsed_mode == "left" or parsed_mode == "l":
            parsed_mode = "l"
        elif parsed_mode == "right" or parsed_mode == "r":
            parsed_mode = "r"
        else:
            return ("interp", "malformed origin")

        try:
            verbal = False
            for c in parsed_date:
                if not c.isdigit():
                    verbal = True
                    break

            if verbal:
                delta = verbal_interpret(parsed_date, today)
                if isinstance(delta, ValueError):
                    return ("interp", "verbal interpretation error")
                shifted_date = today + datetime.timedelta(days=delta)
                assembly_year = shifted_date.year
                assembly_month = shifted_date.month
                assembly_day = shifted_date.day
            else:
                if len(parsed_date) == 4:
                    assembly_month = int(parsed_date[0:2])
                    assembly_day = parsed_date[2:4]
                    if today_month < assembly_month:
                        assembly_year = today_year + 1
                    else:
                        assembly_year = today_year
                elif len(parsed_date) == 8:
                    assembly_year = parsed_date[0:4]
                    assembly_month = parsed_date[4:6]
                    assembly_day = parsed_date[6:8]
                else:
                    return ("interp", "malformed date")
        except Exception as ex:
            return ex

        try:
            assembly_hour = parsed_time[0:2]
            assembly_minute = parsed_time[2:4]
        except Exception:
            return ("interp", "malformed time")

        try:
            parsed_date_time = datetime.datetime(
                int(assembly_year),
                int(assembly_month),
                int(assembly_day),
                int(assembly_hour),
                int(assembly_minute),
            )
            if parsed_date_time < datetime.datetime.now():
                return ("interp", "date has passed")
            else:
                return [parsed_origin, parsed_date_time, parsed_mode]
        except Exception as ex:
            return ("interp", "date interpretaiton error")

    except Exception as ex:
        return ("unknown", "unknown runtime error")


import os

QUERY_DIR = "C:/Users/**replaced ALIAS using filter-repo**/Desktop/github/yshttl/program/book_queries"
EMAIL = "**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**
QUERY_PREFIX = "query_"

#'{:_<10}'.format('test')
# test______

dirs = os.listdir(f"{QUERY_DIR}/{EMAIL}")


if len(dirs) == 0:
    index_formatted = "{:0<2}".format(int(0))
    file = open(f"{QUERY_DIR}/{EMAIL}/{QUERY_PREFIX + index_formatted}.json", "w")
else:
    i = 0
    while i < len(dirs):
        dirs[i] = int(dirs[i].split("_")[1][:-5])
        i += 1

    i = 0
    j = 0
    while i < len(dirs):
        if j < dirs[i]:
            print(j)
            break
        i += 1
        j += 1

    index_formatted = "{:0>2}".format(int(j))
    file = open(f"{QUERY_DIR}/{EMAIL}/{QUERY_PREFIX + index_formatted}.json", "w")
