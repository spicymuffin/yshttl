import base64
import rsa
import json
import requests

# need to log into ys portal through:
# https://portal.yonsei.ac.kr/passni/spLogin.jsp
# =================== OR =====================
# https://portal.yonsei.ac.kr/SSOLegacy.do

# region constants

S1_pad = len('S1"         value="')
S1_len = len('34175A69027670C2C2B2ED852C9E1E2BD357330DE5A3D487CC24BC7324F8446B1FC345098B59C7FA28BB41737D7E5A545BA85F7B7116C9148E74EA7D515587FBECA9653CB01D8F985C7BE7052E004505AA3DA0EC4822C5BE3E348640C138612A0BBCDA1FA0532F06AD0F3D0BEC3B8CF61AFE9F6F340A606021C503323FD553EDA561838AA63D92827897AB91B4FF380C41B3E1DA45B2AC55740C9757F398575FC08634B168B580B2A6B906090AE5D007DD7F2A062B63FBCFED0A10F3D103B4B2C9E07255D2659B63E3E624F37986E902A02720AAF914BD027A6D437A0017A6EF2F052470888FC59DE716D61105F8DD92F35EAEDFD682F189735C04356829BE50')

RSAPublicKey2_pad = len("', '")
RSAPublicKey2_len = len("10001")

ssoChallenge_pad = len("var ssoChallenge= '")


spLogin_request_data = {
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

spLogin_request = requests.get(
    'https://portal.yonsei.ac.kr/passni/spLogin.jsp', headers=spLogin_request_data)

s = spLogin_request.headers["Set-Cookie"]
# print(s)
# print(PmSSOAuthService_request.content.decode())
# print(PmSSOAuthService_request.headers)
# find cookie vals
__smVisitorID1_cookie_name = "__smVisitorID"
__smVisitorID1 = ""
index = s.rfind(__smVisitorID1_cookie_name) + \
    len(__smVisitorID1_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID1 += s[index]
    index += 1

JSESSIONID1_cookie_name = "JSESSIONID"
JSESSIONID1 = ""
index = s.find(JSESSIONID1_cookie_name) + \
    len(JSESSIONID1_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID1 += s[index]
    index += 1


SSOLegacy_request1_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

SSOLegacy_request1_headers = {
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

SSOLegacy_request1_data = {
    'retUrl': '',
    'failUrl': '',
    'ssoGubun': 'Redirect',
    'a': 'aaaa',
    'b': 'bbbb',
}

SSOLegacy_request1 = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do',
                                   cookies=SSOLegacy_request1_cookies, headers=SSOLegacy_request1_headers, data=SSOLegacy_request1_data)

SSOLegacy_request_content1 = SSOLegacy_request1.content.decode()
S1_start_index1 = SSOLegacy_request_content1.rfind("S1") + S1_pad
S11 = SSOLegacy_request_content1[S1_start_index1:S1_start_index1 + S1_len]


PmSSOService1_request_headers = {
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

PmSSOService1_request_data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'S1': S11,
    'loginUrl': '',
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb',
}

PmSSOService1_request = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService',
                                      headers=PmSSOService1_request_headers, data=PmSSOService1_request_data)

s = PmSSOService1_request.headers["Set-Cookie"]
# print(s)
# print(PmSSOAuthService_request.content.decode())
# print(PmSSOAuthService_request.headers)
# find cookie vals
__smVisitorID2_cookie_name = "__smVisitorID"
__smVisitorID2 = ""
index = s.rfind(__smVisitorID2_cookie_name) + \
    len(__smVisitorID2_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID2 += s[index]
    index += 1

JSESSIONID2_cookie_name = "JSESSIONID"
JSESSIONID2 = ""
index = s.find(JSESSIONID2_cookie_name) + \
    len(JSESSIONID2_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID2 += s[index]
    index += 1


logindo_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

logindo_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Referer': 'https://portal.yonsei.ac.kr/ui/index.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

logindo_request = requests.get('https://portal.yonsei.ac.kr/portal/MainCtr/login.do',
                               cookies=logindo_request_cookies, headers=logindo_request_headers)


spLogin1_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

spLogin1_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Referer': 'https://portal.yonsei.ac.kr/ui/index.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

spLogin1_request = requests.get('https://portal.yonsei.ac.kr/passni/spLogin.jsp',
                                cookies=spLogin1_request_cookies, headers=spLogin1_request_headers)


# endregion


SSOLegacy_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

SSOLegacy_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

SSOLegacy_request_data = {
    'retUrl': '',
    'failUrl': '',
    'ssoGubun': 'Redirect',
    'a': 'aaaa',
    'b': 'bbbb',
}

SSOLegacy_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do',
                                  cookies=SSOLegacy_request_cookies, headers=SSOLegacy_request_headers, data=SSOLegacy_request_data)


# region SSOLegacy_request dissect
SSOLegacy_request_content = SSOLegacy_request.content.decode()
S1_start_index = SSOLegacy_request_content.rfind("S1") + S1_pad
S1 = SSOLegacy_request_content[S1_start_index:S1_start_index + S1_len]
# endregion

# region PmSSOService data

PmSSOService_request_cookies = {
    'JSESSIONID': JSESSIONID2,
    '__smVisitorID': __smVisitorID2,
}

PmSSOService_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'JSESSIONID=xwOcz4ux87aOJFWfYxM9CuT6A2ADkGis4AcQb7Cm1nkNsWy9xZifOOaNpZlgi8fX.amV1c19kb21haW4vc3NvMV8x; __smVisitorID=sD5xQPjpKul',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

PmSSOService_request_data = {
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

# endregion

PmSSOService_request = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService',
                                     cookies=PmSSOService_request_cookies, headers=PmSSOService_request_headers, data=PmSSOService_request_data)

# print(PmSSOService_request.content.decode())
# region PmSSOService_request dissect
PmSSOService_request_content = PmSSOService_request.content.decode()
scan_i = PmSSOService_request_content.rfind(
    "rsa.setPublic")

while PmSSOService_request_content[scan_i] != "'":
    scan_i += 1
scan_i += 1

RSAPublicKey1 = ""
while PmSSOService_request_content[scan_i] != "'":
    RSAPublicKey1 += PmSSOService_request_content[scan_i]
    scan_i += 1
scan_i += 1

while PmSSOService_request_content[scan_i] != "'":
    scan_i += 1
scan_i += 1

RSAPublicKey2 = ""
while PmSSOService_request_content[scan_i] != "'":
    RSAPublicKey2 += PmSSOService_request_content[scan_i]
    scan_i += 1

ssoChallenge_start_index = PmSSOService_request_content.find(
    "var ssoChallenge= '") + ssoChallenge_pad
ssoChallenge = ""
while PmSSOService_request_content[ssoChallenge_start_index] != "'":
    ssoChallenge += PmSSOService_request_content[ssoChallenge_start_index]
    ssoChallenge_start_index += 1

# endregion


userid = "**replaced USERID using filter-repo**"
userpw = "**replaced PW using filter-repo**"

jsonObj = {'userid': userid, 'userpw': userpw, 'ssoChallenge': ssoChallenge}

y = json.dumps(jsonObj, separators=(',', ':'))
message = str(y)

publicKeyHex = (RSAPublicKey1, RSAPublicKey2)
publicKey = rsa.PublicKey(int(publicKeyHex[0], 16), int(publicKeyHex[1], 16))

encMsg = rsa.encrypt(message.encode(), publicKey)


PmSSOAuthService_request_cookies = {
    'JSESSIONID': JSESSIONID2,
    '__smVisitorID': __smVisitorID2,
}

PmSSOAuthService_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'JSESSIONID=xwOcz4ux87aOJFWfYxM9CuT6A2ADkGis4AcQb7Cm1nkNsWy9xZifOOaNpZlgi8fX.amV1c19kb21haW4vc3NvMV8x; __smVisitorID=sD5xQPjpKul',
    'Origin': 'https://infra.yonsei.ac.kr',
    'Referer': 'https://infra.yonsei.ac.kr/sso/PmSSOService',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

PmSSOAuthService_request_data = [
    ('app_id', 'nportalYonsei'),
    ('retUrl', 'https://portal.yonsei.ac.kr:443'),
    ('failUrl', 'https://portal.yonsei.ac.kr:443'),
    ('baseUrl', 'https://portal.yonsei.ac.kr:443'),
    ('loginUrl', ''),
    ('loginType', 'invokeID'),
    ('E2', encMsg.hex()),
    ('E3', ''),
    ('E4', ''),
    ('ssoGubun', 'Redirect'),
    ('refererUrl', 'https://portal.yonsei.ac.kr/passni/spLogin.jsp'),
    ('a', 'aaaa'),
    ('b', 'bbbb'),
    ('loginId', ''),
    ('loginPasswd', ''),
    ('loginId', ''),
]

PmSSOAuthService_request = requests.post(
    "https://infra.yonsei.ac.kr/sso/PmSSOAuthService", cookies=PmSSOAuthService_request_cookies, headers=PmSSOAuthService_request_headers, data=PmSSOAuthService_request_data)

PmSSOAuthService_request_content = PmSSOAuthService_request.content.decode()
# print(PmSSOAuthService_request_content)

print(scan_i)
print(PmSSOAuthService_request_content)

scan_i = PmSSOAuthService_request_content.find(
    '"E3"       value=') + len('"E3"       value=') + 1
E3 = ""
while PmSSOAuthService_request_content[scan_i] != '"':
    E3 += PmSSOAuthService_request_content[scan_i]
    scan_i += 1

scan_i = PmSSOAuthService_request_content.find(
    '"E4"       value=') + len('"E4"       value=') + 1
E4 = ""
while PmSSOAuthService_request_content[scan_i] != '"':
    E4 += PmSSOAuthService_request_content[scan_i]
    scan_i += 1

scan_i = PmSSOAuthService_request_content.find(
    '"S2"       value=') + len('"S2"       value=') + 1
S2 = ""
while PmSSOAuthService_request_content[scan_i] != '"':
    S2 += PmSSOAuthService_request_content[scan_i]
    scan_i += 1

scan_i = PmSSOAuthService_request_content.find(
    '"CLTID"    value=') + len('"CLTID"    value=') + 1
CLTID = ""
while PmSSOAuthService_request_content[scan_i] != '"':
    CLTID += PmSSOAuthService_request_content[scan_i]
    scan_i += 1

print(E3)
print(E4)
print(S2)
print(CLTID)

SSOLegacydopnamespLoginData_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

SSOLegacydopnamespLoginData_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Origin': 'https://infra.yonsei.ac.kr',
    'Referer': 'https://infra.yonsei.ac.kr/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

SSOLegacydopnamespLoginData_request_params = {
    'pname': 'spLoginData',
}

SSOLegacydopnamespLoginData_request_data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'loginUrl': '',
    'E3': E3,
    'E4': E4,
    'S2': S2,
    'CLTID': CLTID,
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb',
}

SSOLegacydopnamespLoginData_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do', params=SSOLegacydopnamespLoginData_request_params,
                                                    cookies=SSOLegacydopnamespLoginData_request_cookies, headers=SSOLegacydopnamespLoginData_request_headers, data=SSOLegacydopnamespLoginData_request_data)
print(SSOLegacydopnamespLoginData_request.headers)


spLoginProcessjsp1_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

spLoginProcessjsp1_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

spLoginProcessjsp1_request = requests.get('http://portal.yonsei.ac.kr/passni/spLoginProcess.jsp',
                                          cookies=spLoginProcessjsp1_request_cookies, headers=spLoginProcessjsp1_request_headers, verify=False)


spLoginProcessjsp2_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

spLoginProcessjsp2_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

spLoginProcessjsp2_request = requests.get('https://portal.yonsei.ac.kr/passni/spLoginProcess.jsp',
                                          cookies=spLoginProcessjsp2_request_cookies, headers=spLoginProcessjsp2_request_headers)


j_login_ssodo_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

j_login_ssodo_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Referer': 'https://portal.yonsei.ac.kr/passni/spLoginProcess.jsp',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

j_login_ssodo_request = requests.get('https://portal.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do',
                                     cookies=j_login_ssodo_request_cookies, headers=j_login_ssodo_request_headers)


indexdo_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

indexdo_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
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

indexdo_request = requests.get('https://portal.yonsei.ac.kr/portal/MainCtr/index.do',
                               cookies=indexdo_request_cookies, headers=indexdo_request_headers)


mainjsp_request_cookies = {
    '__smVisitorID': __smVisitorID1,
    'JSESSIONID': JSESSIONID1,
}

mainjsp_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=GrR1r_Bc3-2; JSESSIONID=9ZnJuMjemELqykRSs2p0rp13VCye9x794k5fsbifRiw1LQsIxu0c1xNhrBkHun3B.amV1c19kb21haW4vcG9ydGFsMV8x',
    'Referer': 'https://portal.yonsei.ac.kr/portal/MainCtr/index.do',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

mainjsp_request = requests.get('https://portal.yonsei.ac.kr/ui/thirdparty/portal/main.jsp',
                               cookies=mainjsp_request_cookies, headers=mainjsp_request_headers)
print(mainjsp_request.headers["Set-Cookie"])
