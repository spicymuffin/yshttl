import requests

import requests

import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    'Referer': 'https://portal.yonsei.ac.kr/ui/index.html',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

islogin = requests.get('https://portal.yonsei.ac.kr/passni/spLogin.jsp', headers=headers)

s = islogin.headers["Set-Cookie"]
#print(s)
# print(PmSSOAuthService_request.content.decode())
# print(PmSSOAuthService_request.headers)
# find cookie vals
__smVisitorID_cookie_name = "__smVisitorID"
__smVisitorID = ""
index = s.rfind(__smVisitorID_cookie_name) + \
    len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID += s[index]
    index += 1

print(__smVisitorID)

JSESSIONID_cookie_name = "JSESSIONID"
JSESSIONID = ""
index = s.find(JSESSIONID_cookie_name) + \
    len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID += s[index]
    index += 1

print(JSESSIONID)

import requests

cookies = {
    '__smVisitorID': __smVisitorID,
    'JSESSIONID': JSESSIONID,
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'retUrl': '',
    'failUrl': '',
    'ssoGubun': 'Redirect',
    'a': 'aaaa',
    'b': 'bbbb',
}

SSOLegacy_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do', cookies=cookies, headers=headers, data=data)
#print(SSOLegacy_request.content.decode())

S1_pad = len('S1"         value="')
S1_len = len('34175A69027670C2C2B2ED852C9E1E2BD357330DE5A3D487CC24BC7324F8446B1FC345098B59C7FA28BB41737D7E5A545BA85F7B7116C9148E74EA7D515587FBECA9653CB01D8F985C7BE7052E004505AA3DA0EC4822C5BE3E348640C138612A0BBCDA1FA0532F06AD0F3D0BEC3B8CF61AFE9F6F340A606021C503323FD553EDA561838AA63D92827897AB91B4FF380C41B3E1DA45B2AC55740C9757F398575FC08634B168B580B2A6B906090AE5D007DD7F2A062B63FBCFED0A10F3D103B4B2C9E07255D2659B63E3E624F37986E902A02720AAF914BD027A6D437A0017A6EF2F052470888FC59DE716D61105F8DD92F35EAEDFD682F189735C04356829BE50')

SSOLegacy_request_content = SSOLegacy_request.content.decode()
S1_start_index = SSOLegacy_request_content.rfind("S1") + S1_pad
S1 = SSOLegacy_request_content[S1_start_index:S1_start_index + S1_len]

print(S1)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'S1': S1,
    'loginUrl': '',
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb',
}

response2 = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService', headers=headers, data=data)
print(response2.headers)

s = response2.headers["Set-Cookie"]
__smVisitorID_cookie_name = "__smVisitorID"
__smVisitorID = ""
index = s.rfind(__smVisitorID_cookie_name) + \
    len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID += s[index]
    index += 1

print(__smVisitorID)

JSESSIONID_cookie_name = "JSESSIONID"
JSESSIONID = ""
index = s.find(JSESSIONID_cookie_name) + \
    len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID += s[index]
    index += 1

print(JSESSIONID)