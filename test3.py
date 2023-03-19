import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/ui/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'listCnt': '3',
    'currPage': '1',
}


response = requests.post(
    'https://portal.yonsei.ac.kr/com/lgin/SsoCtr/isLogin.do', headers=headers, data=data)

s = response.headers["Set-Cookie"]
# find cookie vals
__smVisitorID_cookie_name = "__smVisitorID"
__smVisitorID_length = len("jyzO4zEkrL1")
index = s.rfind(__smVisitorID_cookie_name)
__smVisitorID = s[index+len(__smVisitorID_cookie_name)+1:index +
                  __smVisitorID_length+len(__smVisitorID_cookie_name)+1]

JSESSIONID_cookie_name = "JSESSIONID"
JSESSIONID_length = len(
    "gfTagH0rZlueeLmsWKternK7GMhE5t1OQmg8cblPTVfOidLxx0QKWaFiWy3f7Ab1.amV1c19kb21haW4vcG9ydGFsMV8x")
index = s.find(JSESSIONID_cookie_name)
JSESSIONID = s[index+len(JSESSIONID_cookie_name)+1:index +
               JSESSIONID_length+len(JSESSIONID_cookie_name)+1]
print(__smVisitorID)
print(JSESSIONID)

cookies = {
    '__smVisitorID': __smVisitorID,
    'JSESSIONID': JSESSIONID,
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=g2siQHZujNM; JSESSIONID=wiRtWNabvBQiyuNJCGaLPrNCJ67YdXAvQTWIbSDSbVXHgrbIxw8GlPZmE1w2kh7Z.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Referer': 'https://portal.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://portal.yonsei.ac.kr/portal/MainCtr/index.do', cookies=cookies, headers=headers)

print(response.headers)
