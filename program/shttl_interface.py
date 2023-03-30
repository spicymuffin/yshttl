import requests
import os
import urllib

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.txt"
CONFIG_FILE_PATH = CURR_PATH + '\\' + CONFIG_FILE_NAME
COOKIE_JAR_FILE_NAME = "cookie_jar.txt"
COOKIE_JAR_FILE_PATH = CURR_PATH + '\\' + COOKIE_JAR_FILE_NAME

WMONID = ""
JSESSIONID = ""

# open and read the file after the appending:
with open(COOKIE_JAR_FILE_PATH, "r") as file:
    WMONID = file.readline()[:-1]
    JSESSIONID = file.readline()

print(WMONID + JSESSIONID)


class data_buider():
    def __init__(self) -> None:
        self.ds = ""

    def ds_append(self, _name, _value) -> str:
        if self.ds != "":
            self.ds += "&"
        self.ds += urllib.parse.quote(_name)
        self.ds += "="
        self.ds += urllib.parse.quote(_value)
        return self.ds


def gen_get_shttls_list_data_string(_areaDivCd, _stdrDt, _resvePosblDt, _seatDivCd, _areaDivCd2, _stdrDt2, _userDivCd, _d_hashtag, _d_one_hastag, _tp):
    """_summary_

    Args:
        _areaDivCd (_type_): _description_
        _stdrDt (_type_): _description_
        _resvePosblDt (_type_): _description_
        _seatDivCd (_type_): _description_
        _areaDivCd2 (_type_): _description_
        _stdrDt2 (_type_): _description_
        _userDivCd (_type_): _description_
        _d_hashtag (_type_): _description_
        _d_one_hastag (_type_): _description_
        _tp (_type_): _description_
    """
    db = data_buider()

    # vars
    menuId = "MTA3NDkwNzI0MDIyNjk1MTQwMDA="
    menuNm = ""
    pgmId = "MzI5MzAyNzI4NzE="
    areaDivCd = _areaDivCd
    stdrDt = _stdrDt
    resvePosblDt = _resvePosblDt
    seatDivCd = _seatDivCd
    areaDivCd2 = _areaDivCd2
    stdrDt2 = _stdrDt2
    userDivCd = _userDivCd
    d_hashtag = _d_hashtag
    d_one_hastag = _d_one_hastag
    tp = _tp

    # names
    menuId_name = "_menuId"
    menuNm_name = "_menuNm"
    pgmId_name = "_pgmId"
    areaDivCd_name = "@d1#areaDivCd"
    stdrDt_name = "@d1#stdrDt"
    resvePosblDt_name = "@d1#resvePosblDt"
    seatDivCd_name = "@d1#seatDivCd"
    areaDivCd2_name = "@d1#areaDivCd2"
    stdrDt2_name = "@d1#stdrDt2"
    userDivCd_name = "@d1#userDivCd"
    d_hashtag_name = "@d#"
    d_one_hastag_name = "@d1#"
    tp_name = "@d1#tp"

    # region samples
    # sample data pack
    '''
    _menuId: MTA3NDkwNzI0MDIyNjk1MTQwMDA=
    _menuNm:
    _pgmId: MzI5MzAyNzI4NzE=
    @d1#areaDivCd: I
    @d1#stdrDt: 20230330
    @d1#resvePosblDt: 1
    @d1#seatDivCd: 1
    @d1#areaDivCd2:
    @d1#stdrDt2: 20230330
    @d1#userDivCd: 12
    @d#: @d1#
    @d1#: dmCond
    @d1#tp: dm
    '''
    # sample url-encoded data pack
    '''
    _menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23stdrDt=20230330&%40d1%23resvePosblDt=1&%40d1%23seatDivCd=1&%40d1%23areaDivCd2=&%40d1%23stdrDt2=20230330&%40d1%23userDivCd=12&%40d%23=%40d1%23&%40d1%23=dmCond&%40d1%23tp=dm&
    '''

    # endregion

    # build data_string
    db.ds_append(menuId_name, menuId)
    db.ds_append(menuNm_name, menuNm)
    db.ds_append(pgmId_name, pgmId)
    db.ds_append(areaDivCd_name, areaDivCd)
    db.ds_append(stdrDt_name,  stdrDt)
    db.ds_append(resvePosblDt_name, resvePosblDt)
    db.ds_append(seatDivCd_name, seatDivCd)
    db.ds_append(areaDivCd2_name, areaDivCd2)
    db.ds_append(stdrDt2_name, stdrDt2)
    db.ds_append(userDivCd_name, userDivCd)
    db.ds_append(d_hashtag_name, d_hashtag)
    db.ds_append(d_one_hastag_name, d_one_hastag)
    db.ds_append(tp_name, tp)

    return db.ds

def gen_book_shttl_data_string(_areaDivCd, _busCd, _busNm, _seatNo, _stdrDt, _beginTm, _endTm, _tm, _seatDivCd, _userDivCd, _persNo):
    # vars
    findSavedRow = "areaDivCd, busCd, seatNo, stdrDt, beginTm"
    menuId = "MTA3NDkwNzI0MDIyNjk1MTQwMDA="
    menuNm = ""
    pgmId = "MzI5MzAyNzI4NzE="
    areaDivCd = _areaDivCd
    busCd = _busCd
    busNm = _busNm
    seatNo = _seatNo
    stdrDt = _stdrDt
    beginTm = _beginTm
    endTm = _endTm
    tm = _tm
    seatDivCd = _seatDivCd
    userDivCd = _userDivCd
    persNo = _persNo
    # region samples
    # sample data pack
    '''
    _findSavedRow: areaDivCd, busCd, seatNo, stdrDt, beginTm
    _menuId: MTA3NDkwNzI0MDIyNjk1MTQwMDA=
    _menuNm: 
    _pgmId: MzI5MzAyNzI4NzE=
    @d1#areaDivCd: I
    @d1#busCd: I4
    @d1#busNm: 4호차
    @d1#seatNo: 
    @d1#stdrDt: 20230331
    @d1#beginTm: 0700
    @d1#endTm: 0800
    @d1#tm: 07:00 ~ 08:00
    @d1#seatDivCd: 
    @d1#userDivCd: 
    @d1#persNo: 
    @d1#thrstNm: 영종대교, 인천대교
    @d1#remrk: 
    @d1#remndSeat: 17
    @d1#resveWaitPcnt: 5
    @d1#resveYn: 0
    @d1#resveWaitYn: 0
    @d1#resveResnDivCd: 1
    @d1#dailResvePosblYn: 1
    @d1#areaDivCd__origin: I
    @d1#busCd__origin: I4
    @d1#seatNo__origin: 
    @d1#stdrDt__origin: 20230331
    @d1#beginTm__origin: 0700
    @d1#sts: u
    @d#: @d1#
    @d1#: dsShtl110
    @d1#tp: ds
    @d2#gbn: P
    @d2#seatDivCd: 1
    @d2#userDivCd: 12
    @d#: @d2#
    @d2#: dmCond
    @d2#tp: dm
    '''
    # sample url-encoded data pack
    '''
    _findSavedRow=areaDivCd%2C%20busCd%2C%20seatNo%2C%20stdrDt%2C%20beginTm&_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23busCd=I4&%40d1%23busNm=4%ED%98%B8%EC%B0%A8&%40d1%23seatNo=&%40d1%23stdrDt=20230331&%40d1%23beginTm=0700&%40d1%23endTm=0800&%40d1%23tm=07%3A00%20~%2008%3A00&%40d1%23seatDivCd=&%40d1%23userDivCd=&%40d1%23persNo=&%40d1%23thrstNm=%EC%98%81%EC%A2%85%EB%8C%80%EA%B5%90%2C%20%EC%9D%B8%EC%B2%9C%EB%8C%80%EA%B5%90&%40d1%23remrk=&%40d1%23remndSeat=17&%40d1%23resveWaitPcnt=5&%40d1%23resveYn=0&%40d1%23resveWaitYn=0&%40d1%23resveResnDivCd=1&%40d1%23dailResvePosblYn=1&%40d1%23areaDivCd__origin=I&%40d1%23busCd__origin=I4&%40d1%23seatNo__origin=&%40d1%23stdrDt__origin=20230331&%40d1%23beginTm__origin=0700&%40d1%23sts=u&%40d%23=%40d1%23&%40d1%23=dsShtl110&%40d1%23tp=ds&%40d2%23gbn=P&%40d2%23seatDivCd=1&%40d2%23userDivCd=12&%40d%23=%40d2%23&%40d2%23=dmCond&%40d2%23tp=dm&
    '''
    # endregion

s = gen_get_shttls_list_data_string(
    "I", "20230331", "1", "1", "", "20230330", "12", "@d1#", "dmCond", "dm")
print(s)


def get_shttl_list(_WMONID, _JSESSIONID, _data_string):
    findShtlbusResveList_do_cookies = {
        'WMONID': _WMONID,
        'JSESSIONID': _JSESSIONID,
    }

    findShtlbusResveList_do_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'WMONID=DsBn5ycHBH4; JSESSIONID=QTzE1aAJoMlQ91AdR6bC7Royi76NkuQAxsPdQCw24u34D1pmxog1pmwolhKfO1CU.amV1c19kb21haW4vaGFrc2EyXzE=',
        'Origin': 'https://underwood1.yonsei.ac.kr',
        'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    findShtlbusResveList_do_data = _data_string

    findShtlbusResveList_do_response = requests.post(
        'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/findShtlbusResveList.do',
        cookies=findShtlbusResveList_do_cookies,
        headers=findShtlbusResveList_do_headers,
        data=findShtlbusResveList_do_data,
    )

    return findShtlbusResveList_do_response.content.decode()


#r = get_shttl_list(WMONID, JSESSIONID, s)

# with open("sample_reserve_list_unparsed.txt", "r") as file:
#     r = file.readline()[:-1]

r = '''{"dsShtl110":[{"resveWaitPcnt":5,"remndSeat":18,"busNm":"4호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"0800","dailResvePosblYn":"1","tm":"07:00 ~ 08:00","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I4","beginTm":"0700"},{"resveWaitPcnt":5,"remndSeat":19,"busNm":"5호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"0820","dailResvePosblYn":"1","tm":"07:20 ~ 08:20","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I5","beginTm":"0720"},{"resveWaitPcnt":5,"remndSeat":9,"busNm":"6호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"0840","dailResvePosblYn":"1","tm":"07:40 ~ 08:40","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I6","beginTm":"0740"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"1호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"0930","dailResvePosblYn":"1","tm":"08:30 ~ 09:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I1","beginTm":"0830"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"2호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1030","dailResvePosblYn":"1","tm":"09:30 ~ 10:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I2","beginTm":"0930"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"3호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1130","dailResvePosblYn":"1","tm":"10:30 ~ 11:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I3","beginTm":"1030"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"4호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1230","dailResvePosblYn":"1","tm":"11:30 ~ 12:30","thrstNm":"경인고속도로","areaDivCd":"I","busCd":"I4","beginTm":"1130"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"5호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1330","dailResvePosblYn":"1","tm":"12:30 ~ 13:30","thrstNm":"경인고속도로","areaDivCd":"I","busCd":"I5","beginTm":"1230"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"6호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1530","dailResvePosblYn":"1","tm":"14:30 ~ 15:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I6","beginTm":"1430"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"1호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1610","dailResvePosblYn":"1","tm":"15:10 ~ 16:10","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I1","beginTm":"1510"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"2호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1730","dailResvePosblYn":"1","tm":"16:30 ~ 17:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I2","beginTm":"1630"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"3호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1810","dailResvePosblYn":"1","tm":"17:10 ~ 18:10","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I3","beginTm":"1710"},{"resveWaitPcnt":0,"remndSeat":0,"busNm":"5호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1910","dailResvePosblYn":"1","tm":"18:10 ~ 19:10","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I5","beginTm":"1810"},{"resveWaitPcnt":4,"remndSeat":0,"busNm":"6호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"1930","dailResvePosblYn":"1","tm":"18:30 ~ 19:30","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I6","beginTm":"1830"},{"resveWaitPcnt":5,"remndSeat":36,"busNm":"1호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"2000","dailResvePosblYn":"1","tm":"19:00 ~ 20:00","thrstNm":"영종대교, 인천대교","areaDivCd":"I","busCd":"I1","beginTm":"1900"},{"resveWaitPcnt":5,"remndSeat":40,"busNm":"2호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"2040","dailResvePosblYn":"1","tm":"19:40 ~ 20:40","thrstNm":"경인고속도로","areaDivCd":"I","busCd":"I2","beginTm":"1940"},{"resveWaitPcnt":5,"remndSeat":40,"busNm":"3호차","remrk":null,"resveYn":0,"resveResnDivCd":null,"stdrDt":"20230331","resveWaitYn":0,"endTm":"2100","dailResvePosblYn":"1","tm":"20:00 ~ 21:00","thrstNm":"경인고속도로","areaDivCd":"I","busCd":"I3","beginTm":"2000"}]}'''

def parse_shttl_list(sl):
    index = 0
    while sl[index] != "[":
        index += 1
    index += 1 #skip [
    bus_l = []
    bus_n = 0
    while index < len(sl):
        if sl[index] == '{':
            bus_l.append("")
        elif sl[index] == '}':
            bus_n += 1
            index += 1
        elif sl[index] == ']':
            break
        else:
            bus_l[bus_n] += sl[index]
        index += 1

    for i in range(len(bus_l)):
        bus = bus_l[i]
        d0 = dict()
        key = ""
        value = ""
        j = 0
        while j < len(bus):
            # control write state
            if bus[j] == '"':
                j += 1
                while bus[j] != '"':
                    key += bus[j]
                    j += 1
            j += 1
            j += 1
            if bus[j] == '"':
                j += 1
                while j < len(bus) and bus[j] != '"':
                    value += bus[j]
                    j += 1
                j+=1
            else:
                while j < len(bus) and bus[j] != ',':
                    value += bus[j]
                    j += 1
                # value = int(value)
            j += 1
            d0[key] = value
            bus_l[i] = d0
            value = ""
            key = ""
    return bus_l

d = parse_shttl_list(r)


for b in d:
    print(b)
