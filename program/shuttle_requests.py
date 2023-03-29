import requests

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())

def get_shttl_list():
    findShtlbusResveList_do_cookies = {
        'WMONID': WMONID,
        'JSESSIONID': ,
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

    findShtlbusResveList_do_data = '_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23stdrDt=20230330&%40d1%23resvePosblDt=1&%40d1%23seatDivCd=1&%40d1%23areaDivCd2=&%40d1%23stdrDt2=20230331 &%40d1%23userDivCd=12&%40d%23=%40d1%23&%40d1%23=dmCond&%40d1%23tp=dm&'

    findShtlbusResveList_do_response = requests.post(
        'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/findShtlbusResveList.do',
        cookies=findShtlbusResveList_do_cookies,
        headers=findShtlbusResveList_do_headers,
        data=findShtlbusResveList_do_data,
    )

    print(findShtlbusResveList_do_response.content.decode())
