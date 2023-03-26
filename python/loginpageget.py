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

JSESSIONID_cookie_name = "JSESSIONID"
__smVisitorID_cookie_name = "__smVisitorID"
cugubun_cookie_name = "cugubun"
UbiResult_cookie_name = "UbiResult"
WMONID_cookie_name = "WMONID"

ssoChallenge_pad = len("var ssoChallenge= '")

PRINT_DISSECT_VALS = False
# endregion

# region pre-login
# region spLoginjsp_request data
spLoginjsp_request_data = {
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
# endregion

spLoginjsp_request = requests.get(
    'https://portal.yonsei.ac.kr/passni/spLogin.jsp', headers=spLoginjsp_request_data)

# region dissect spLoginjsp_request
s = spLoginjsp_request.headers["Set-Cookie"]
__smVisitorID_main = ""
index = s.rfind(__smVisitorID_cookie_name) + \
    len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID_main += s[index]
    index += 1

JSESSIONID_main = ""
index = s.find(JSESSIONID_cookie_name) + \
    len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID_main += s[index]
    index += 1
# endregion

# region SSOLegacydo_prelogin_request data
SSOLegacydo_prelogin_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
}

SSOLegacy_prelogin_request_headers = {
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

SSOLegacy_prelogin_request_data = {
    'retUrl': '',
    'failUrl': '',
    'ssoGubun': 'Redirect',
    'a': 'aaaa',
    'b': 'bbbb',
}
# endregion

SSOLegacydo_prelogin_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do',
                                             cookies=SSOLegacydo_prelogin_request_cookies, headers=SSOLegacy_prelogin_request_headers, data=SSOLegacy_prelogin_request_data)

# region dissect SSOLegacydo_prelogin_request
SSOLegacydo_prelogin_request_content = SSOLegacydo_prelogin_request.content.decode()
index = SSOLegacydo_prelogin_request_content.rfind("S1") + S1_pad
S1_prelogin = SSOLegacydo_prelogin_request_content[index:index + S1_len]
# endregion

# region PmSSOService_prelogin_request data
PmSSOService_prelogin_request_headers = {
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

PmSSOService_prelogin_request_data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'S1': S1_prelogin,
    'loginUrl': '',
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb',
}
# endregion

PmSSOService_prelogin_request = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService',
                                              headers=PmSSOService_prelogin_request_headers, data=PmSSOService_prelogin_request_data)

# region dissect PmSSOService_prelogin_request
s = PmSSOService_prelogin_request.headers["Set-Cookie"]

__smVisitorID_auth = ""
index = s.rfind(__smVisitorID_cookie_name) + \
    len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID_auth += s[index]
    index += 1

JSESSIONID_auth = ""
index = s.find(JSESSIONID_cookie_name) + \
    len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID_auth += s[index]
    index += 1
# endregion

# region logindo_request data
logindo_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
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
# endregion

logindo_request = requests.get('https://portal.yonsei.ac.kr/portal/MainCtr/login.do',
                               cookies=logindo_request_cookies, headers=logindo_request_headers)

# region spLoginjsp1 data
spLoginjsp1_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
}

spLoginjsp1_request_headers = {
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
# endregion

spLoginjsp1_request = requests.get('https://portal.yonsei.ac.kr/passni/spLogin.jsp',
                                   cookies=spLoginjsp1_request_cookies, headers=spLoginjsp1_request_headers)

# region SSOLegacy_request data
SSOLegacydo_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
}

SSOLegacydo_request_headers = {
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

SSOLegacydo_request_data = {
    'retUrl': '',
    'failUrl': '',
    'ssoGubun': 'Redirect',
    'a': 'aaaa',
    'b': 'bbbb',
}
# endregion

SSOLegacydo_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do',
                                    cookies=SSOLegacydo_request_cookies, headers=SSOLegacydo_request_headers, data=SSOLegacydo_request_data)

# region SSOLegacydo_request dissect
SSOLegacydo_request_content = SSOLegacydo_request.content.decode()
s_i = SSOLegacydo_request_content.rfind("S1") + S1_pad
S1 = SSOLegacydo_request_content[s_i:s_i + S1_len]
# endregion

# region PmSSOService data
PmSSOService_request_cookies = {
    'JSESSIONID': JSESSIONID_auth,
    '__smVisitorID': __smVisitorID_auth,
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
# endregion

# region authentication
userid = "**replaced USERID using filter-repo**"
userpw = "**replaced PW using filter-repo**"

jsonObj = {'userid': userid, 'userpw': userpw, 'ssoChallenge': ssoChallenge}

y = json.dumps(jsonObj, separators=(',', ':'))
message = str(y)

publicKeyHex = (RSAPublicKey1, RSAPublicKey2)
publicKey = rsa.PublicKey(int(publicKeyHex[0], 16), int(publicKeyHex[1], 16))

encMsg = rsa.encrypt(message.encode(), publicKey)
# endregion

# region post-login
# region PmSSOAuthService_request data
PmSSOAuthService_request_cookies = {
    'JSESSIONID': JSESSIONID_auth,
    '__smVisitorID': __smVisitorID_auth,
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
# endregion

PmSSOAuthService_request = requests.post(
    "https://infra.yonsei.ac.kr/sso/PmSSOAuthService", cookies=PmSSOAuthService_request_cookies, headers=PmSSOAuthService_request_headers, data=PmSSOAuthService_request_data)

# region PmSSOAuthService_request dissect
PmSSOAuthService_request_content = PmSSOAuthService_request.content.decode()

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
if PRINT_DISSECT_VALS:
    print(E3)
    print(E4)
    print(S2)
    print(CLTID)
# endregion

# region SSOLegacydopnamespLoginData_request data
SSOLegacydopnamespLoginData_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
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
# endregion

SSOLegacydopnamespLoginData_request = requests.post('https://portal.yonsei.ac.kr/SSOLegacy.do', params=SSOLegacydopnamespLoginData_request_params,
                                                    cookies=SSOLegacydopnamespLoginData_request_cookies, headers=SSOLegacydopnamespLoginData_request_headers, data=SSOLegacydopnamespLoginData_request_data)

# region spLoginProcessjsp_postlogin1_request data
spLoginProcessjsp_postlogin1_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
}

spLoginProcessjsp_postlogin1_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=s1k9Oq6x1-J; JSESSIONID=xhF99xsOgA6H5eOjY0T4Ry5CZ7R71gzT4cyCp3KBK198TT8yxlmJJTqauyxlu6cH.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

# endregion

spLoginProcessjsp_postlogin1_request = requests.get('http://portal.yonsei.ac.kr/passni/spLoginProcess.jsp',
                                                    cookies=spLoginProcessjsp_postlogin1_request_cookies, headers=spLoginProcessjsp_postlogin1_request_headers, verify=False)

# region spLoginProcessjsp_postlogin2_request data
spLoginProcessjsp_postlogin2_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
}

spLoginProcessjsp_postlogin2_request_headers = {
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
# endregion

spLoginProcessjsp_postlogin2_request = requests.get('https://portal.yonsei.ac.kr/passni/spLoginProcess.jsp',
                                                    cookies=spLoginProcessjsp_postlogin2_request_cookies, headers=spLoginProcessjsp_postlogin2_request_headers)

# region j_login_ssodo_request data
j_login_ssodo_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
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
# endregion

j_login_ssodo_request = requests.get('https://portal.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do',
                                     cookies=j_login_ssodo_request_cookies, headers=j_login_ssodo_request_headers)

# region indexdo_request data
indexdo_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
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
# endregion

indexdo_request = requests.get('https://portal.yonsei.ac.kr/portal/MainCtr/index.do',
                               cookies=indexdo_request_cookies, headers=indexdo_request_headers)

# region mainjsp_request data
mainjsp_request_cookies = {
    '__smVisitorID': __smVisitorID_main,
    'JSESSIONID': JSESSIONID_main,
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
# endregion

mainjsp_request = requests.get('https://portal.yonsei.ac.kr/ui/thirdparty/portal/main.jsp',
                               cookies=mainjsp_request_cookies, headers=mainjsp_request_headers)
# endregion

print(mainjsp_request.headers["Set-Cookie"])

# region mainjsp_request dissect
s = mainjsp_request.headers["Set-Cookie"]
scan_i = s.find(cugubun_cookie_name)+len(cugubun_cookie_name)+1
cugubun = ""
while s[scan_i] != ";":
    cugubun += s[scan_i]
    scan_i += 1

scan_i = s.find(UbiResult_cookie_name)+len(UbiResult_cookie_name)+1
UbiResult = ""
while s[scan_i] != ";":
    UbiResult += s[scan_i]
    scan_i += 1

if PRINT_DISSECT_VALS:
    print(cugubun)
    print(UbiResult)
# endregion

print(__smVisitorID_main)
print(JSESSIONID_main)
print(cugubun)
print(UbiResult)

# region underwood1_WMONID_request data
underwood1_WMONID_request_cookies = {
    'JSESSIONID': JSESSIONID_main,
    'cugubun': cugubun,
    'UbiResult': UbiResult,
}

underwood1_WMONID_request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=cKQzlfUkLV9QYqLifyjfQmqduTJfg1Y8Vaat5TT0UqjItOmIxOLsDD71lbpjAkAy.amV1c19kb21haW4vaGFrc2ExXzE=; cugubun=FWoNcShBVqMoCNAVKOMoCNBWQIIi; UbiResult=DAh6COsSmpnYfeRSQ0OkbQ==',
    'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do?locale=ko',
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

underwood1_WMONID_request_params = {
    'link': 'shuttle',
}
# endregion

underwood1_WMONID_request = requests.get(
    'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do',
    params=underwood1_WMONID_request_params,
    cookies=underwood1_WMONID_request_cookies,
    headers=underwood1_WMONID_request_headers,
)
s = underwood1_WMONID_request.headers["Set-Cookie"]
scan_i = s.find(WMONID_cookie_name) + len(WMONID_cookie_name) + 1
WMONID = ""

while s[scan_i] != ";":
    WMONID += s[scan_i]
    scan_i+= 1

print(underwood1_WMONID_request.headers)
print(WMONID)

# region test

# cookies = {
#     'cugubun': cugubun,
#     'UbiResult': UbiResult,
#     'WMONID': 'VznSh_9GCE4',
#     'JSESSIONID': JSESSIONID_main,
# }

# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     # 'Cookie': 'cugubun=JYrRfQiAbtocKpIhetocKpJikomE; UbiResult=MRxhvwJB/cG8+H9KsVmYpg==; WMONID=VznSh_9GCE4; JSESSIONID=L74lx2VzQhcHhXnKtvrEdGrveQ6TMOmn4WYwznrfXyU8TKKEx9lmZ6QSa3aeVacW.amV1c19kb21haW4vaGFrc2ExXzE=',
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

# data = '_menuId=MTA3NDkwNzI0MDIyNjk1MTQwMDA%3D&_menuNm=&_pgmId=MzI5MzAyNzI4NzE%3D&%40d1%23areaDivCd=I&%40d1%23stdrDt=20230327&%40d1%23resvePosblDt=2&%40d1%23seatDivCd=1&%40d1%23areaDivCd2=&%40d1%23stdrDt2=20230325&%40d1%23userDivCd=12&%40d%23=%40d1%23&%40d1%23=dmCond&%40d1%23tp=dm&'

# response = requests.post(
#     'https://underwood1.yonsei.ac.kr/sch/shtl/ShtlrmCtr/findShtlbusResveList.do',
#     cookies=cookies,
#     headers=headers,
#     data=data,
# )
# endregion
