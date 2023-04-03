import requests
import ast
import urllib

WMONID = ""
JSESSIONID = ""

DEBUG = 0


class AuthError(Exception):
    pass


class data_string_buider():
    def __init__(self) -> None:
        self.ds = ""

    def ds_append(self, _name, _value) -> str:
        if self.ds != "":
            self.ds += "&"
        self.ds += urllib.parse.quote(_name)
        self.ds += "="
        self.ds += urllib.parse.quote(_value)
        return self.ds


# region request handlers
# region request_get_shttl_list
def gen_data_string_request_shttl_list(_areaDivCd, _stdrDt, _resvePosblDt="2", _seatDivCd="1", _areaDivCd2="", _stdrDt2="12312312", _userDivCd="12", _d_hashtag="@d1#", _d_one_hastag="dmCond", _tp="dm"):
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
    dsb = data_string_buider()

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
    dsb.ds_append(menuId_name, menuId)
    dsb.ds_append(menuNm_name, menuNm)
    dsb.ds_append(pgmId_name, pgmId)
    dsb.ds_append(areaDivCd_name, areaDivCd)
    dsb.ds_append(stdrDt_name,  stdrDt)
    dsb.ds_append(resvePosblDt_name, resvePosblDt)
    dsb.ds_append(seatDivCd_name, seatDivCd)
    dsb.ds_append(areaDivCd2_name, areaDivCd2)
    dsb.ds_append(stdrDt2_name, stdrDt2)
    dsb.ds_append(userDivCd_name, userDivCd)
    dsb.ds_append(d_hashtag_name, d_hashtag)
    dsb.ds_append(d_one_hastag_name, d_one_hastag)
    dsb.ds_append(tp_name, tp)

    return dsb.ds


def request_shttl_list(_data_string):
    findShtlbusResveList_do_cookies = {
        'WMONID': WMONID,
        'JSESSIONID': JSESSIONID,
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


def parse_request_shttl_list(resp):
    index = 0
    while resp[index] != "[":
        index += 1
    index += 1  # skip [
    bus_l = []
    bus_n = 0
    while index < len(resp):
        if resp[index] == '{':
            bus_l.append("")
        elif resp[index] == '}':
            bus_n += 1
            index += 1
        elif resp[index] == ']':
            break
        else:
            bus_l[bus_n] += resp[index]
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
                j += 1
            else:
                while j < len(bus) and bus[j] != ',':
                    value += bus[j]
                    j += 1
                # value = int(value)
            j += 1
            d0[key] = value
            value = ""
            key = ""
        bus_l[i] = d0
    return bus_l
# endregion


# region request_book_shttl
def gen_data_string_request_book_shttl(_d1_areaDivCd, _d1_busCd, _d1_busNm, _d1_stdrDt, _d1_beginTm, _d1_endTm, _d1_tm, _d1_thrstNm, _d1_remrk, _d1_remndSeat, _d1_resveWaitPcnt, _d1_resveYn, _d1_resveWaitYn, _d1_resveResnDivCd, _d1_dailResvePosblYn, _d1_areaDivCd__origin, _d1_busCd__origin, _d1_stdrDt__origin, _d1_beginTm__origin, _d2_seatDivCd, _d2_userDivCd, _d2_empty, _d2_tp):
    dsb = data_string_buider()

    # vars
    d1_findSavedRow = "areaDivCd, busCd, seatNo, stdrDt, beginTm"
    d1_menuId = "MTA3NDkwNzI0MDIyNjk1MTQwMDA="
    d1_menuNm = ""
    d1_pgmId = "MzI5MzAyNzI4NzE="
    d1_areaDivCd = _d1_areaDivCd
    d1_busCd = _d1_busCd
    d1_busNm = _d1_busNm
    d1_seatNo = ""
    d1_stdrDt = _d1_stdrDt
    d1_beginTm = _d1_beginTm
    d1_endTm = _d1_endTm
    d1_tm = _d1_tm
    d1_seatDivCd = ""
    d1_userDivCd = ""
    d1_persNo = ""
    d1_thrstNm = _d1_thrstNm
    d1_remrk = _d1_remrk
    d1_remndSeat = _d1_remndSeat
    d1_resveWaitPcnt = _d1_resveWaitPcnt
    d1_resveYn = _d1_resveYn
    d1_resveWaitYn = _d1_resveWaitYn
    d1_resveResnDivCd = _d1_resveResnDivCd
    d1_dailResvePosblYn = _d1_dailResvePosblYn
    d1_areaDivCd__origin = _d1_areaDivCd__origin
    d1_busCd__origin = _d1_busCd__origin
    d1_seatNo__origin = ""
    d1_stdrDt__origin = _d1_stdrDt__origin
    d1_beginTm__origin = _d1_beginTm__origin
    d1_sts = "u"
    d1_d_hashtag = "@d1#"
    d1_empty = "dsShtl110"
    d1_tp = "ds"
    d2_gbn = "P"
    d2_seatDivCd = _d2_seatDivCd
    d2_userDivCd = _d2_userDivCd
    d2_d_hashtag = "@d2#"
    d2_empty = _d2_empty  # is @d1# from find query
    d2_tp = _d2_tp  # is @d1#tp from find query

    # names
    d1_findSavedRow_name = "_findSavedRow"
    d1_menuId_name = "_menuId"
    d1_menuNm_name = "_menuNm"
    d1_pgmId_name = "_pgmId"
    d1_areaDivCd_name = "@d1#areaDivCd"
    d1_busCd_name = "@d1#busCd"
    d1_busNm_name = "@d1#busNm"
    d1_seatNo_name = "@d1#seatNo"
    d1_stdrDt_name = "@d1#stdrDt"
    d1_beginTm_name = "@d1#beginTm"
    d1_endTm_name = "@d1#endTm"
    d1_tm_name = "@d1#tm"
    d1_seatDivCd_name = "@d1#seatDivCd"
    d1_userDivCd_name = "@d1#userDivCd"
    d1_persNo_name = "@d1#persNo"
    d1_thrstNm_name = "@d1#thrstNm"
    d1_remrk_name = "@d1#remrk"
    d1_remndSeat_name = "@d1#remndSeat"
    d1_resveWaitPcnt_name = "@d1#resveWaitPcnt"
    d1_resveYn_name = "@d1#resveYn"
    d1_resveWaitYn_name = "@d1#resveWaitYn"
    d1_resveResnDivCd_name = "@d1#resveResnDivCd"
    d1_dailResvePosblYn_name = "@d1#dailResvePosblYn"
    d1_areaDivCd__origin_name = "@d1#areaDivCd__origin"
    d1_busCd__origin_name = "@d1#busCd__origin"
    d1_seatNo__origin_name = "@d1#seatNo__origin"
    d1_stdrDt__origin_name = "@d1#stdrDt__origin"
    d1_beginTm__origin_name = "@d1#beginTm__origin"
    d1_sts_name = "@d1#sts"
    d1_d_hashtag_name = "@d#"
    d1_empty_name = "@d1#"
    d1_tp_name = "@d1#tp"
    d2_gbn_name = "@d2#gbn"
    d2_seatDivCd_name = "@d2#seatDivCd"
    d2_userDivCd_name = "@d2#userDivCd"
    d2_d_hashtag_name = "@d#"
    d2_empty_name = "@d2#"
    d2_tp_name = "@d2#tp"

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

    # build data_string

    dsb.ds_append(d1_findSavedRow_name, d1_findSavedRow)
    dsb.ds_append(d1_menuId_name, d1_menuId)
    dsb.ds_append(d1_menuNm_name, d1_menuNm)
    dsb.ds_append(d1_pgmId_name, d1_pgmId)
    dsb.ds_append(d1_areaDivCd_name, d1_areaDivCd)
    dsb.ds_append(d1_busCd_name, d1_busCd)
    dsb.ds_append(d1_busNm_name, d1_busNm)
    dsb.ds_append(d1_seatNo_name, d1_seatNo)
    dsb.ds_append(d1_stdrDt_name, d1_stdrDt)
    dsb.ds_append(d1_beginTm_name, d1_beginTm)
    dsb.ds_append(d1_endTm_name, d1_endTm)
    dsb.ds_append(d1_tm_name, d1_tm)
    dsb.ds_append(d1_seatDivCd_name, d1_seatDivCd)
    dsb.ds_append(d1_userDivCd_name, d1_userDivCd)
    dsb.ds_append(d1_persNo_name, d1_persNo)
    dsb.ds_append(d1_thrstNm_name, d1_thrstNm)
    dsb.ds_append(d1_remrk_name, d1_remrk)
    dsb.ds_append(d1_remndSeat_name, d1_remndSeat)
    dsb.ds_append(d1_resveWaitPcnt_name, d1_resveWaitPcnt)
    dsb.ds_append(d1_resveYn_name, d1_resveYn)
    dsb.ds_append(d1_resveWaitYn_name, d1_resveWaitYn)
    dsb.ds_append(d1_resveResnDivCd_name, d1_resveResnDivCd)
    dsb.ds_append(d1_dailResvePosblYn_name, d1_dailResvePosblYn)
    dsb.ds_append(d1_areaDivCd__origin_name, d1_areaDivCd__origin)
    dsb.ds_append(d1_busCd__origin_name, d1_busCd__origin)
    dsb.ds_append(d1_seatNo__origin_name, d1_seatNo__origin)
    dsb.ds_append(d1_stdrDt__origin_name, d1_stdrDt__origin)
    dsb.ds_append(d1_beginTm__origin_name, d1_beginTm__origin)
    dsb.ds_append(d1_sts_name, d1_sts)
    dsb.ds_append(d1_d_hashtag_name, d1_d_hashtag)
    dsb.ds_append(d1_empty_name, d1_empty)
    dsb.ds_append(d1_tp_name, d1_tp)
    dsb.ds_append(d2_gbn_name, d2_gbn)
    dsb.ds_append(d2_seatDivCd_name, d2_seatDivCd)
    dsb.ds_append(d2_userDivCd_name, d2_userDivCd)
    dsb.ds_append(d2_d_hashtag_name, d2_d_hashtag)
    dsb.ds_append(d2_empty_name, d2_empty)
    dsb.ds_append(d2_tp_name, d2_tp)

    return dsb.ds


def request_book_shttl(_data_string):
    saveShtlbusResveList_do_cookies = {
        'WMONID': WMONID,
        'JSESSIONID': JSESSIONID,
    }

    saveShtlbusResveList_do_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'WMONID=N38l9lUXcEb; cugubun=EVvQjSkCameUAVyVgieUAVzWmcSG; UbiResult=MRxhvwJB/cG8+H9KsVmYpg==; JSESSIONID=I7gYqQZLAKeJkCeEbewwj1n1S4yNy5q1vodDqT7ASKmkkM5UxY9NBhlbCKYloBqv.amV1c19kb21haW4vaGFrc2ExXzE=',
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

    saveShtlbusResveList_do_data = _data_string

    saveShtlbusResveList_do_response = requests.post(
        'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/saveShtlbusResveList.do',
        cookies=saveShtlbusResveList_do_cookies,
        headers=saveShtlbusResveList_do_headers,
        data=saveShtlbusResveList_do_data,
    )

    return saveShtlbusResveList_do_response.content.decode()
# endregion


# region request user_info
def request_user_info():
    check_login_state_r_cookies = {
        'WMONID': WMONID,
        'JSESSIONID': JSESSIONID,
    }
    check_login_state_r_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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
    check_login_state_r_data = '_menuId=MzMzODYzMjY%3D&_menuNm=&_pgmId=MTg3NDA2&'
    check_login_state_r_response = requests.post(
        'https://underwood1.yonsei.ac.kr/com/cnst/PropCtr/findViewSession.do',
        cookies=check_login_state_r_cookies,
        headers=check_login_state_r_headers,
        data=check_login_state_r_data,
    )
    return check_login_state_r_response.content.decode()
# endregion
# endregion

# region high level wrappers


def get_shttl_list(_origin, _departure_datetime):
    ds = gen_data_string_request_shttl_list(_origin, _departure_datetime)
    r = request_shttl_list(ds)
    #print(r)
    d = parse_request_shttl_list(r)

    if DEBUG:
        for b in d:
            print("bus change!!!!!!!!!!!!!!!")
            for key, value in b.items():
                print(f"{key}: {value}")

    return d


def book_shttl(_data):
    ds = gen_data_string_request_book_shttl(_data["areaDivCd"],
                                            _data["busCd"],
                                            _data["busNm"],
                                            _data["stdrDt"],
                                            _data["beginTm"],
                                            _data["endTm"],
                                            _data["tm"],
                                            _data["thrstNm"],
                                            _data["remrk"],
                                            _data["remndSeat"],
                                            _data["resveWaitPcnt"],
                                            _data["resveYn"],
                                            _data["resveWaitYn"],
                                            _data["resveResnDivCd"],
                                            _data["dailResvePosblYn"],
                                            _data["areaDivCd"],
                                            _data["busCd"],
                                            _data["stdrDt"],
                                            _data["beginTm"],
                                            "1",
                                            "12",
                                            "dmCond",
                                            "dm")

    r = request_book_shttl(ds)

    print(r)


def check_login():
    r = request_user_info()
    r = r.replace("true", "True")
    d0 = ast.literal_eval(r)
    if DEBUG:
        print(d0)
    return True if d0["dmLoginConfirm"]["isLogin"] == "1" else False
# endregion
