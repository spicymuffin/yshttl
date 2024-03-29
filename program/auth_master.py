import requests
import rsa
import json

# region names
JSESSIONID_cookie_name = "JSESSIONID"
__smVisitorID_cookie_name = "__smVisitorID"
WMONID_cookie_name = "WMONID"
# endregion


def get_auth_cookies(_userid, _userpw, PRINT_DISSECT_VALS=False, NOTIFY_ERRORS=False):
    """ get authenticated cookies from underwood1.yonsei.ac.kr

    Args:
        _userid (string): user identificator (학번)
        _userpw (string): user password

    Returns:
        tuple or Exception: WMONID and JSESSIONID if successful (tuple), else exception (Exception)
    """
    try:
        # region spLogin_jsp_r
        spLogin_jsp_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        spLogin_jsp_r_response = requests.get(
            'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp?returnUrl=L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl&locale={locale}',
            headers=spLogin_jsp_r_headers,
        )
        # endregion

        # region dissect spLogin_jsp_r
        s = spLogin_jsp_r_response.headers["Set-Cookie"]
        WMONID = ""
        index = s.rfind(WMONID_cookie_name) + \
            len(WMONID_cookie_name) + 1  # this is a mess sorry
        while (s[index] != ';'):
            WMONID += s[index]
            index += 1

        JSESSIONID_main = ""
        index = s.find(JSESSIONID_cookie_name) + \
            len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
        while (s[index] != ';'):
            JSESSIONID_main += s[index]
            index += 1

        if PRINT_DISSECT_VALS:
            print("WMONID:", WMONID, '\n')
            print("JSESSIONID_main:", JSESSIONID_main, '\n')
        # endregion

        # region SSOLegacy_do_prelogin_r
        SSOLegacy_do_prelogin_r_cookies = {
            'WMONID': WMONID,
            'JSESSIONID': JSESSIONID_main,
        }

        SSOLegacy_do_prelogin_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://underwood1.yonsei.ac.kr',
            'Referer': 'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        SSOLegacy_do_prelogin_r_data = {
            'retUrl': '',
            'failUrl': '',
            'ssoGubun': 'Redirect',
            'a': 'aaaa',
            'b': 'bbbb',
        }

        SSOLegacy_do_prelogin_r_response = requests.post('https://underwood1.yonsei.ac.kr/SSOLegacy.do',
                                                         cookies=SSOLegacy_do_prelogin_r_cookies,
                                                         headers=SSOLegacy_do_prelogin_r_headers,
                                                         data=SSOLegacy_do_prelogin_r_data)
        # endregion

        # region dissect SSOLegacy_do_prelogin_r
        SSOLegacydo_prelogin_request_content = SSOLegacy_do_prelogin_r_response.content.decode()
        scan_i = SSOLegacydo_prelogin_request_content.rfind(
            '"S1"         value="') + len('"S1"         value="')
        S1_prelogin = ""
        while SSOLegacydo_prelogin_request_content[scan_i] != '"':
            S1_prelogin += SSOLegacydo_prelogin_request_content[scan_i]
            scan_i += 1
        if PRINT_DISSECT_VALS:
            print("S1_prelogin:", S1_prelogin, '\n')
        # endregion

        # region PmSSOService_r
        PmSSOService_r_cookies = {

        }

        PmSSOService_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://underwood1.yonsei.ac.kr',
            'Referer': 'https://underwood1.yonsei.ac.kr/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        PmSSOService_r_data = {
            'app_id': 'haksaYonsei',
            'retUrl': 'https://underwood1.yonsei.ac.kr:443',
            'failUrl': 'https://underwood1.yonsei.ac.kr:443',
            'baseUrl': 'https://underwood1.yonsei.ac.kr:443',
            'S1': S1_prelogin,
            'loginUrl': '',
            'ssoGubun': 'Redirect',
            'refererUrl': 'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp',
            'a': 'aaaa',
            'b': 'bbbb',
        }

        PmSSOService_r_response = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService',
                                                cookies=PmSSOService_r_cookies,
                                                headers=PmSSOService_r_headers,
                                                data=PmSSOService_r_data)
        # endregion

        # region dissect PmSSOService_r
        s = PmSSOService_r_response.headers["Set-Cookie"]
        __smVisitorID_main = ""
        index = s.rfind(__smVisitorID_cookie_name) + \
            len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
        while (s[index] != ';'):
            __smVisitorID_main += s[index]
            index += 1

        JSESSIONID_temp = ""
        index = s.find(JSESSIONID_cookie_name) + \
            len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
        while s[index] != ';':
            JSESSIONID_temp += s[index]
            index += 1

        # if an error occurs
        PmSSOService_r_response_content = PmSSOService_r_response.content.decode()
        if PmSSOService_r_response_content.find("연동대상시스템의 정상적인 요청이 아닙니다") != -1:
            if NOTIFY_ERRORS:
                print("연동대상시스템의 정상적인 요청이 아닙니다 error occured while authenticating")
            return get_auth_cookies(_userid, _userpw)

        scan_i = PmSSOService_r_response_content.rfind(
            "rsa.setPublic")

        while PmSSOService_r_response_content[scan_i] != "'":
            scan_i += 1
        scan_i += 1

        RSAPublicKey1 = ""
        while PmSSOService_r_response_content[scan_i] != "'":
            RSAPublicKey1 += PmSSOService_r_response_content[scan_i]
            scan_i += 1
        scan_i += 1

        while PmSSOService_r_response_content[scan_i] != "'":
            scan_i += 1
        scan_i += 1

        RSAPublicKey2 = ""
        while PmSSOService_r_response_content[scan_i] != "'":
            RSAPublicKey2 += PmSSOService_r_response_content[scan_i]
            scan_i += 1

        ssoChallenge_start_index = PmSSOService_r_response_content.find(
            "var ssoChallenge= '") + len("var ssoChallenge= '")
        ssoChallenge = ""
        while PmSSOService_r_response_content[ssoChallenge_start_index] != "'":
            ssoChallenge += PmSSOService_r_response_content[ssoChallenge_start_index]
            ssoChallenge_start_index += 1
        if PRINT_DISSECT_VALS:
            print("__smVisitorID_main:", __smVisitorID_main, '\n')
            print("JSESSIONID_temp:", JSESSIONID_temp, '\n')
            print("RSAPublicKey1:", RSAPublicKey1, '\n')
            print("RSAPublicKey2:", RSAPublicKey2, '\n')
            print("ssoChallenge:", ssoChallenge, '\n')
        # endregion

        # region authentication
        userid = _userid
        userpw = _userpw

        jsonObj = {'userid': userid, 'userpw': userpw,
                   'ssoChallenge': ssoChallenge}

        y = json.dumps(jsonObj, separators=(',', ':'))
        message = str(y)

        publicKeyHex = (RSAPublicKey1, RSAPublicKey2)
        publicKey = rsa.PublicKey(
            int(publicKeyHex[0], 16), int(publicKeyHex[1], 16))

        encMsg = rsa.encrypt(message.encode(), publicKey)
        # endregion

        # region PmSSOAuthService_r
        PmSSOAuthService_r_cookies = {
            'JSESSIONID': JSESSIONID_temp,
            '__smVisitorID': __smVisitorID_main,
        }

        PmSSOAuthService_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
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

        PmSSOAuthService_r_data = [
            ('app_id', 'haksaYonsei'),
            ('retUrl', 'https://underwood1.yonsei.ac.kr:443'),
            ('failUrl', 'https://underwood1.yonsei.ac.kr:443'),
            ('baseUrl', 'https://underwood1.yonsei.ac.kr:443'),
            ('loginUrl', ''),
            ('loginType', 'invokeID'),
            ('E2', encMsg.hex()),
            ('E3', ''),
            ('E4', ''),
            ('ssoGubun', 'Redirect'),
            ('refererUrl',
             'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp?returnUrl=L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl&locale={locale}'),
            ('a', 'aaaa'),
            ('b', 'bbbb'),
            ('returnUrl', 'L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl'),
            ('locale', '{locale}'),
            ('loginId', ''),
            ('loginPasswd', ''),
            ('loginId', ''),
        ]

        PmSSOAuthService_r_response = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOAuthService',
                                                    cookies=PmSSOAuthService_r_cookies, headers=PmSSOAuthService_r_headers, data=PmSSOAuthService_r_data)
        # endregion

        # region PmSSOAuthService_r dissect
        PmSSOAuthService_r_response_content = PmSSOAuthService_r_response.content.decode()

        scan_i = PmSSOAuthService_r_response_content.find('"E3"       value=')

        # credential validity check
        if scan_i == -1:
            return "invalid user credentials"

        scan_i = PmSSOAuthService_r_response_content.find(
            '"E3"       value=') + len('"E3"       value=') + 1
        E3 = ""
        while PmSSOAuthService_r_response_content[scan_i] != '"':
            E3 += PmSSOAuthService_r_response_content[scan_i]
            scan_i += 1

        scan_i = PmSSOAuthService_r_response_content.find(
            '"E4"       value=') + len('"E4"       value=') + 1
        E4 = ""
        while PmSSOAuthService_r_response_content[scan_i] != '"':
            E4 += PmSSOAuthService_r_response_content[scan_i]
            scan_i += 1

        scan_i = PmSSOAuthService_r_response_content.find(
            '"S2"       value=') + len('"S2"       value=') + 1
        S2 = ""
        while PmSSOAuthService_r_response_content[scan_i] != '"':
            S2 += PmSSOAuthService_r_response_content[scan_i]
            scan_i += 1

        scan_i = PmSSOAuthService_r_response_content.find(
            '"CLTID"    value=') + len('"CLTID"    value=') + 1
        CLTID = ""
        while PmSSOAuthService_r_response_content[scan_i] != '"':
            CLTID += PmSSOAuthService_r_response_content[scan_i]
            scan_i += 1

        if PRINT_DISSECT_VALS:
            print("E3:", E3, '\n')
            print("E4:", E4, '\n')
            print("S2:", S2, '\n')
            print("CLTID:", CLTID, '\n')
        # endregion

        # region SSOLegacy_do_pname_spLogin_r
        SSOLegacy_do_pname_spLogin_r_cookies = {
            'WMONID': WMONID,
            'JSESSIONID': JSESSIONID_main,
        }

        SSOLegacy_do_pname_spLogin_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
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

        SSOLegacy_do_pname_spLogin_r_params = {
            'pname': 'spLoginData',
        }

        SSOLegacy_do_pname_spLogin_r_data = {
            'app_id': 'haksaYonsei',
            'retUrl': 'https://underwood1.yonsei.ac.kr:443',
            'failUrl': 'https://underwood1.yonsei.ac.kr:443',
            'baseUrl': 'https://underwood1.yonsei.ac.kr:443',
            'loginUrl': '',
            'E3': E3,
            'E4': E4,
            'S2': S2,
            'CLTID': CLTID,
            'ssoGubun': 'Redirect',
            'refererUrl': 'https://underwood1.yonsei.ac.kr/passni/spLogin.jsp?returnUrl=L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl&locale={locale}',
            'a': 'aaaa',
            'b': 'bbbb',
            'returnUrl': 'L2NvbS9sZ2luL1Nzb0N0ci9pbml0RXh0UGFnZVdvcmsuZG8/bGluaz1zaHV0dGxl',
            'locale': '{locale}',
        }

        SSOLegacy_do_pname_spLogin_r_response = requests.post('https://underwood1.yonsei.ac.kr/SSOLegacy.do',
                                                              params=SSOLegacy_do_pname_spLogin_r_params,
                                                              cookies=SSOLegacy_do_pname_spLogin_r_cookies,
                                                              headers=SSOLegacy_do_pname_spLogin_r_headers,
                                                              data=SSOLegacy_do_pname_spLogin_r_data)
        # endregion

        # region spLoginProcess_jsp_1_r
        spLoginProcess_jsp_1_r_cookies = {
            'WMONID': WMONID,
            'JSESSIONID': JSESSIONID_main,
        }

        spLoginProcess_jsp_1_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        spLoginProcess_jsp_1_r_response = requests.get(
            'http://underwood1.yonsei.ac.kr/passni/spLoginProcess.jsp',
            cookies=spLoginProcess_jsp_1_r_cookies,
            headers=spLoginProcess_jsp_1_r_headers,
            verify=False,
        )
        # endregion

        # region spLoginProcess_jsp_2_r
        spLoginProcess_jsp_2_r_cookies = {
            'WMONID': 'DsBn5ycHBH4',
            'JSESSIONID': 'Ad411AxBG8p7WaXvORdyIkD9dVj92QGhbWFXbi0Ag510L75OxvaQ2CWKIGA11Mql.amV1c19kb21haW4vaGFrc2EyXzE=',
        }

        spLoginProcess_jsp_2_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        spLoginProcess_jsp_2_r_response = requests.get('https://underwood1.yonsei.ac.kr/passni/spLoginProcess.jsp',
                                                       cookies=spLoginProcess_jsp_2_r_cookies,
                                                       headers=spLoginProcess_jsp_2_r_headers)
        # endregion

        # region j_login_sso_do_r
        j_login_sso_do_r_cookies = {
            'WMONID': WMONID,
            'JSESSIONID': JSESSIONID_main
        }

        j_login_sso_do_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://underwood1.yonsei.ac.kr/passni/spLoginProcess.jsp',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        j_login_sso_do_r_response = requests.get(
            'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do?locale={locale}',
            cookies=j_login_sso_do_r_cookies,
            headers=j_login_sso_do_r_headers,
        )
        # endregion

        # region initExtPageWork_do_r
        initExtPageWork_do_r_cookies = {
            'WMONID': WMONID,
            'JSESSIONID': JSESSIONID_main,
        }

        initExtPageWork_do_r_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do?locale={locale}',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        initExtPageWork_do_r_params = {
            'link': 'shuttle',
        }

        initExtPageWork_do_r_response = requests.get(
            'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do',
            params=initExtPageWork_do_r_params,
            cookies=initExtPageWork_do_r_cookies,
            headers=initExtPageWork_do_r_headers,
        )
        # endregion

    except Exception as ex:
        return ex

    return (WMONID, JSESSIONID_main)
