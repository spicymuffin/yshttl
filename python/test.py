# import requests

# cookies = {
#     'WMONID': 'gbmYHzPC3xQ',
#     'JSESSIONID': 'licewejSfPVwbUL4cElzhWbEoRnsTskqnjrTjW1j0HP999yax31akViWNxOR01aw.amV1c19kb21haW4vaGFrc2EyXzE=',
# }

# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     # 'Cookie': 'WMONID=gbmYHzPC3xQ; _ga=GA1.3.748332228.1680069477; _gid=GA1.3.1219567376.1680069477; JSESSIONID=licewejSfPVwbUL4cElzhWbEoRnsTskqnjrTjW1j0HP999yax31akViWNxOR01aw.amV1c19kb21haW4vaGFrc2EyXzE=; _INSIGHT_CK_8301=80ac3f0625ecc11af35a81e06810a4e3_69476|27f33c18176930db719959265cd9a162_63391:1680165191000; cugubun=HYoNdPmyarAcCNUNVAAcCNVOaASQ; UbiResult=nyalIz1mdzeUGmDT1xnMJw==',
#     'Origin': 'https://underwood1.yonsei.ac.kr',
#     'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
#     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# data = '_findSavedRow=areaDivCd%2C%20busCd%2C%20seatNo%2C%20stdrDt%2C%20beginTm&_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23busCd=I5&%40d1%23busNm=5%ED%98%B8%EC%B0%A8&%40d1%23seatNo=&%40d1%23stdrDt=20230331&%40d1%23beginTm=0720&%40d1%23endTm=0820&%40d1%23tm=07%3A20%20~%2008%3A20&%40d1%23seatDivCd=&%40d1%23userDivCd=&%40d1%23persNo=&%40d1%23thrstNm=%EC%98%81%EC%A2%85%EB%8C%80%EA%B5%90%2C%20%EC%9D%B8%EC%B2%9C%EB%8C%80%EA%B5%90&%40d1%23remrk=&%40d1%23remndSeat=16&%40d1%23resveWaitPcnt=5&%40d1%23resveYn=0&%40d1%23resveWaitYn=0&%40d1%23resveResnDivCd=2&%40d1%23dailResvePosblYn=1&%40d1%23areaDivCd__origin=I&%40d1%23busCd__origin=I5&%40d1%23seatNo__origin=&%40d1%23stdrDt__origin=20230331&%40d1%23beginTm__origin=0720&%40d1%23sts=u&%40d%23=%40d1%23&%40d1%23=dsShtl110&%40d1%23tp=ds&%40d2%23gbn=P&%40d2%23seatDivCd=1&%40d2%23userDivCd=12&%40d%23=%40d2%23&%40d2%23=dmCond&%40d2%23tp=dm'

# response = requests.post(
#     'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/saveShtlbusResveList.do',
#     cookies=cookies,
#     headers=headers,
#     data=data,
# )

# print(response.content.decode())

# import datetime

# year = int(2023)
# month = int(3)
# day = int(5)
# hour = int(12)
# minute = int(23)
# departure_datetime = datetime.datetime(
#     year, month, day, hour, minute)

# print(departure_datetime)
# print(str(departure_datetime.year) + format(departure_datetime.month, "0>2") + format(departure_datetime.day, "0>2"))

# import requests

# cookies = {
#     'WMONID': 'mW5O3G11u0p',
#     'JSESSIONID': 'Jz1Q37zY1Dw7WdU1Fi7j8U3nRUlQwdbSz7KdmMbGkDZvb1XLxVvZVqaSu2HAJIBM.amV1c19kb21haW4vaGFrc2EyXzE=',
# }

# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     # 'Cookie': 'WMONID=mW5O3G11u0p; JSESSIONID=Jz1Q37zY1Dw7WdU1Fi7j8U3nRUlQwdbSz7KdmMbGkDZvb1XLxVvZVqaSu2HAJIBM.amV1c19kb21haW4vaGFrc2EyXzE=',
#     'Origin': 'https://underwood1.yonsei.ac.kr',
#     'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
#     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# data = '_menuId=MzMzODYzMjY%3D&_menuNm=&_pgmId=MTg3NDA2&'

# response = requests.post(
#     'https://underwood1.yonsei.ac.kr/com/cnst/PropCtr/findViewSession.do',
#     cookies=cookies,
#     headers=headers,
#     data=data,
# )

# print(response.content.decode())


# import ast
# #                                                                                                                                                                                                                                                                          !                                                                              !
# r = '{"gdmViewSession":{"msg":"success","userNm":"꾸씩루이지","encStr":"SvRXCvYqst4AsjKIvDSVdnpTiByoar4knruU0j6e9y8=","deptNm":"컴퓨팅계열","locale":"locale","deptCd":"32053","deptTtNm":"컴퓨팅계열","userSupport":"0!@#undefined","clientDevice":"normal","passPwdExpir":True,"persNo":"**replaced USERID using filter-repo**","wasInfo":"운영","socpsCd":"1110","passLoginPolicy":True,"sessionTimeout":3600,"campsDivCd":"G","userDivCd":"12","reltmNtcnRcptnYn":"1","pageZoom":"100"},"dmLoginConfirm":{"isLogin":"1"}}'
# #r = '{"gay":True}'
# d0 = ast.literal_eval(r)
# print(d0)

# a = {"alen": 1, "**replaced ALIAS using filter-repo**": 2, "oleg": 3}

# for i in range(1, len(a.keys())):
#     print(a[a.keys()[i]])

# import datetime

# d1 = datetime.datetime(2023, 4, 1, 5, 45).timestamp()
# d2 = datetime.datetime(2023, 4, 1, 5, 44).timestamp()

# print((d2-d1))

# def a():
#     pass

# b = a

# print(b == a)

import datetime

dt = datetime.datetime.now()

for i in range(14):
    asd = dt + datetime.timedelta(days=i)
    print(asd.weekday())
